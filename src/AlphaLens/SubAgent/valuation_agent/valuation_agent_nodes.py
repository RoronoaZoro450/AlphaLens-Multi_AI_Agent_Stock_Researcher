import json
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from AlphaLens.SubAgent.valuation_agent.valuation_agent_prompt import VALUATION_REPORT_PROMPT
from AlphaLens.SubAgent.valuation_agent.valuation_agent_state import valuationState
from AlphaLens.SubAgent.valuation_agent.valuation_agent_tools import get_company_info, get_dcf_inputs, get_peer_multiples
from AlphaLens.config.llms import get_report_writer_llm , get_llm_for_tools
from AlphaLens.SubAgent.valuation_agent.valuation_agent_model import ValuationModel


valuation_tools = [get_peer_multiples,get_dcf_inputs,get_company_info]
valuation_tools_node = ToolNode(valuation_tools)


def valuation_agent_node(state:valuationState)->valuationState:
    valuation_tools_llm = get_llm_for_tools().bind_tools(valuation_tools)
    response = valuation_tools_llm.invoke(state["messages"])
    return {"messages": [response]}



#=============================================================================================



def compute_val_node(state: valuationState) -> valuationState:
    messages = state['messages']
    data = {}
    for msg in messages:
        if isinstance(msg, ToolMessage):
            try:
                data[msg.name] = json.loads(msg.content)
            except json.JSONDecodeError:
                continue

    company = data.get("get_company_info", {})
    peers   = data.get("get_peer_multiples", {})
    dcf     = data.get("get_dcf_inputs", {})

    def safe(value, default):
        """.get() only falls back when the key is missing — not when the
        value is explicitly None. These tools often store None, so guard both."""
        return value if value is not None else default

    eps            = safe(company.get("eps"), 0)
    book_value     = safe(company.get("book_value"), 0)
    current_price  = safe(company.get("current_price"), 0)
    median_pe      = safe(peers.get("median_pe"), 0)
    beta           = safe(company.get("beta"), 1.0)
    fcf_history    = safe(dcf.get("fcf_history"), {})
    revenue_growth = safe(dcf.get("revenue_growth"), 0.08)
    shares         = safe(dcf.get("shares_outstanding"), 0)   # 0, not 1 — see Bug 3
    debt           = safe(dcf.get("total_debt"), 0)
    cash           = safe(dcf.get("cash"), 0)

    risk_free = 0.045
    erp       = 0.055
    wacc      = round(risk_free + beta * erp, 4)

    # ── DCF ──
    dcf_target = None
    if fcf_history and shares > 0:
        latest_fcf = list(fcf_history.values())[0]
        g = min(float(revenue_growth), 0.20)   # cap restored

        pv_fcfs = 0
        for yr in range(1, 6):
            future_cash_flow = latest_fcf * (1 + g) ** yr
            pv_fcfs += future_cash_flow / (1 + wacc) ** yr

        perpetual_growth = 0.03
        if wacc > perpetual_growth:             # guards divide-by-zero / negative terminal value
            terminal    = (latest_fcf * (1 + g) ** 5 * (1 + perpetual_growth)) / (wacc - perpetual_growth)
            terminal_pv = terminal / (1 + wacc) ** 5
            equity      = pv_fcfs + terminal_pv - debt + cash
            dcf_target  = round(equity / shares, 2)

    # ── Comps ──
    comps_target = round(median_pe * eps, 2) if median_pe and eps else None

    # ── Graham ──
    graham = None
    if eps > 0 and book_value > 0:
        graham = round((22.5 * eps * book_value) ** 0.5, 2)

    # ── Weighted target ──
    methods = {"comps": comps_target, "dcf": dcf_target, "graham": graham}
    weights = {"comps": 0.40, "dcf": 0.40, "graham": 0.20}
    valid   = {k: v for k, v in methods.items() if v and v > 0}

    price_target = None
    if valid:
        total_w      = sum(weights[k] for k in valid)
        price_target = round(sum(v * weights[k] / total_w for k, v in valid.items()), 2)

    # ── Upside / verdict — 
    if price_target and current_price > 0:
        upside  = round((price_target - current_price) / current_price, 4)
        verdict = (
            "Undervalued"   if upside > 0.15  else
            "Overvalued"    if upside < -0.15 else
            "Fairly Valued"
        )
    else:
        upside  = None
        verdict = "Unknown"

    confidence = round(len(valid) / 3, 2)

    computed_valuation = {
        "ticker":        state.get("ticker"),
        "current_price": current_price,
        "comps_target":  comps_target,
        "dcf_target":    dcf_target,
        "graham_number": graham,
        "median_pe":     median_pe,
        "median_pb":     peers.get("median_pb"),
        "median_ev_ebitda": peers.get("median_ev_ebitda"),
        "peer_multiples": peers.get("peers", {}),
        "peers_not_found": peers.get("peers_not_found", []),
        "peers_used":    list(peers.get("peers", {}).keys()),
        "price_target":  price_target,
        "upside_pct":    upside,
        "verdict":       verdict,
        "wacc_used":     wacc,
        "confidence":    confidence,
        "methods_used":  list(valid.keys()),
    }

    return {"computed_valuations": computed_valuation}



#=============================================================================================



def report_node(state: valuationState) -> valuationState:
    computed = state.get("computed_valuations", {})

    formatted_prompt = VALUATION_REPORT_PROMPT.replace(
        "{computed_valuations}",
        json.dumps(computed, indent=2)
    )

    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content="Write the ValuationReport JSON now."),
    ]

    report_writer_llm = get_report_writer_llm().with_structured_output(ValuationModel)

    response = report_writer_llm.invoke(messages)

    return {"result": response.model_dump()}
