"""Fleet economics and cloud cost models."""

from __future__ import annotations

from mlsysim.core.constants import ureg

from ._units import _ensure_unit


def calc_monthly_egress_cost(bytes_per_sec, cost_per_gb):
    """Monthly cloud egress cost from sustained byte rate and $/GB."""
    b_s = _ensure_unit(bytes_per_sec, ureg.byte / ureg.second, "bytes_per_sec")
    monthly_bytes = b_s * (30 * ureg.day)
    cost_rate = _ensure_unit(cost_per_gb, ureg.dollar / ureg.gigabyte, "cost_per_gb")
    cost = monthly_bytes * cost_rate.to(ureg.dollar / ureg.byte)
    return cost.m_as(ureg.dollar)


def calc_fleet_tco(unit_cost, power_w, quantity, years, kwh_price):
    """Total cost of ownership (CapEx + energy OpEx)."""
    u_cost = _ensure_unit(unit_cost, ureg.dollar, "unit_cost")
    p_w = _ensure_unit(power_w, ureg.watt, "power_w")
    price = _ensure_unit(kwh_price, ureg.dollar / ureg.kilowatt_hour, "kwh_price")
    time = _ensure_unit(years, ureg.year, "years")
    fleet_capex = u_cost * quantity
    total_energy = p_w * quantity * time
    power_opex = total_energy * price
    return (fleet_capex + power_opex).m_as(ureg.dollar)
