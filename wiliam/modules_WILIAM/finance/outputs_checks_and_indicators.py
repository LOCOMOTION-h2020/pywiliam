"""
Module finance.outputs_checks_and_indicators
Translated using PySD version 3.10.0
"""


@component.add(
    name="check_finance",
    subscripts=["REGIONS_35_I", "HOUSEHOLDS_I"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "variation_in_households_financial_assets_due_to_net_lending": 1,
        "households_net_lending": 1,
        "variation_in_households_financial_liabilities": 1,
    },
)
def check_finance():
    return (
        variation_in_households_financial_assets_due_to_net_lending()
        - households_net_lending()
        - variation_in_households_financial_liabilities()
    )


@component.add(
    name="check_finance_0",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "check_finance": 1},
)
def check_finance_0():
    return if_then_else(
        time() >= 2015,
        lambda: sum(
            check_finance().rename(
                {"REGIONS_35_I": "REGIONS_35_I!", "HOUSEHOLDS_I": "HOUSEHOLDS_I!"}
            ),
            dim=["REGIONS_35_I!", "HOUSEHOLDS_I!"],
        ),
        lambda: 0,
    )


@component.add(
    name="check_finance_2",
    subscripts=["REGIONS_35_I"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gross_fixed_capital_formation_real": 2,
        "price_gfcf": 2,
        "price_transformation": 2,
        "unit_conversion_dollars_mdollars": 2,
        "increase_in_households_capital_stock_due_to_investments": 2,
        "number_of_households_by_income_and_type": 2,
        "time": 1,
    },
)
def check_finance_2():
    return if_then_else(
        np.logical_or(
            np.abs(
                gross_fixed_capital_formation_real()
                .loc[:, "REAL_ESTATE"]
                .reset_coords(drop=True)
                * price_gfcf().loc[:, "REAL_ESTATE"].reset_coords(drop=True)
                / price_transformation()
                - sum(
                    increase_in_households_capital_stock_due_to_investments().rename(
                        {"HOUSEHOLDS_I": "HOUSEHOLDS_I!"}
                    )
                    * number_of_households_by_income_and_type().rename(
                        {"HOUSEHOLDS_I": "HOUSEHOLDS_I!"}
                    )
                    / unit_conversion_dollars_mdollars(),
                    dim=["HOUSEHOLDS_I!"],
                )
            )
            < 1,
            time() < 2015,
        ),
        lambda: xr.DataArray(
            0, {"REGIONS_35_I": _subscript_dict["REGIONS_35_I"]}, ["REGIONS_35_I"]
        ),
        lambda: np.abs(
            gross_fixed_capital_formation_real()
            .loc[:, "REAL_ESTATE"]
            .reset_coords(drop=True)
            * price_gfcf().loc[:, "REAL_ESTATE"].reset_coords(drop=True)
            / price_transformation()
            - sum(
                increase_in_households_capital_stock_due_to_investments().rename(
                    {"HOUSEHOLDS_I": "HOUSEHOLDS_I!"}
                )
                * number_of_households_by_income_and_type().rename(
                    {"HOUSEHOLDS_I": "HOUSEHOLDS_I!"}
                )
                / unit_conversion_dollars_mdollars(),
                dim=["HOUSEHOLDS_I!"],
            )
        ),
    )


@component.add(
    name="check_finance_3",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "check_households_capital_stock_negatives": 1,
        "check_households_financial_assets_negatives": 1,
        "check_households_liabilities_negatives": 1,
    },
)
def check_finance_3():
    return (
        check_households_capital_stock_negatives()
        + check_households_financial_assets_negatives()
        + check_households_liabilities_negatives()
    )


@component.add(
    name="check_finance_4",
    subscripts=["REGIONS_35_I", "HOUSEHOLDS_I"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "ratio_liabilities_to_assets": 2,
        "check_ratio_liabilities_to_assets": 2,
    },
)
def check_finance_4():
    return if_then_else(
        np.logical_or(
            time() < 2015,
            zidz(ratio_liabilities_to_assets(), check_ratio_liabilities_to_assets()) - 1
            < 0.1,
        ),
        lambda: xr.DataArray(
            0,
            {
                "REGIONS_35_I": _subscript_dict["REGIONS_35_I"],
                "HOUSEHOLDS_I": _subscript_dict["HOUSEHOLDS_I"],
            },
            ["REGIONS_35_I", "HOUSEHOLDS_I"],
        ),
        lambda: zidz(
            ratio_liabilities_to_assets(), check_ratio_liabilities_to_assets()
        ),
    )


@component.add(
    name="check_households_capital_stock_negatives",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"households_capital_stock": 1},
)
def check_households_capital_stock_negatives():
    return sum(
        if_then_else(
            households_capital_stock().rename(
                {"REGIONS_35_I": "REGIONS_35_I!", "HOUSEHOLDS_I": "HOUSEHOLDS_I!"}
            )
            < 0,
            lambda: xr.DataArray(
                1,
                {
                    "REGIONS_35_I!": [
                        "AUSTRIA",
                        "BELGIUM",
                        "BULGARIA",
                        "CROATIA",
                        "CYPRUS",
                        "CZECH_REPUBLIC",
                        "DENMARK",
                        "ESTONIA",
                        "FINLAND",
                        "FRANCE",
                        "GERMANY",
                        "GREECE",
                        "HUNGARY",
                        "IRELAND",
                        "ITALY",
                        "LATVIA",
                        "LITHUANIA",
                        "LUXEMBOURG",
                        "MALTA",
                        "NETHERLANDS",
                        "POLAND",
                        "PORTUGAL",
                        "ROMANIA",
                        "SLOVAKIA",
                        "SLOVENIA",
                        "SPAIN",
                        "SWEDEN",
                        "UK",
                        "CHINA",
                        "EASOC",
                        "INDIA",
                        "LATAM",
                        "RUSSIA",
                        "USMCA",
                        "LROW",
                    ],
                    "HOUSEHOLDS_I!": [
                        "INCOME1_DENSE_SINGLE",
                        "INCOME1_DENSE_SINGLEWCHILDREN",
                        "INCOME1_DENSE_COUPLE",
                        "INCOME1_DENSE_COUPLEWCHILDREN",
                        "INCOME1_DENSE_OTHER",
                        "INCOME1_DENSE_OTHERWCHILDREN",
                        "INCOME1_SPARSE_SINGLE",
                        "INCOME1_SPARSE_SINGLEWCHILDREN",
                        "INCOME1_SPARSE_COUPLE",
                        "INCOME1_SPARSE_COUPLEWCHILDREN",
                        "INCOME1_SPARSE_OTHER",
                        "INCOME1_SPARSE_OTHERWCHILDREN",
                        "INCOME2_DENSE_SINGLE",
                        "INCOME2_DENSE_SINGLEWCHILDREN",
                        "INCOME2_DENSE_COUPLE",
                        "INCOME2_DENSE_COUPLEWCHILDREN",
                        "INCOME2_DENSE_OTHER",
                        "INCOME2_DENSE_OTHERWCHILDREN",
                        "INCOME2_SPARSE_SINGLE",
                        "INCOME2_SPARSE_SINGLEWCHILDREN",
                        "INCOME2_SPARSE_COUPLE",
                        "INCOME2_SPARSE_COUPLEWCHILDREN",
                        "INCOME2_SPARSE_OTHER",
                        "INCOME2_SPARSE_OTHERWCHILDREN",
                        "INCOME3_DENSE_SINGLE",
                        "INCOME3_DENSE_SINGLEWCHILDREN",
                        "INCOME3_DENSE_COUPLE",
                        "INCOME3_DENSE_COUPLEWCHILDREN",
                        "INCOME3_DENSE_OTHER",
                        "INCOME3_DENSE_OTHERWCHILDREN",
                        "INCOME3_SPARSE_SINGLE",
                        "INCOME3_SPARSE_SINGLEWCHILDREN",
                        "INCOME3_SPARSE_COUPLE",
                        "INCOME3_SPARSE_COUPLEWCHILDREN",
                        "INCOME3_SPARSE_OTHER",
                        "INCOME3_SPARSE_OTHERWCHILDREN",
                        "INCOME4_DENSE_SINGLE",
                        "INCOME4_DENSE_SINGLEWCHILDREN",
                        "INCOME4_DENSE_COUPLE",
                        "INCOME4_DENSE_COUPLEWCHILDREN",
                        "INCOME4_DENSE_OTHER",
                        "INCOME4_DENSE_OTHERWCHILDREN",
                        "INCOME4_SPARSE_SINGLE",
                        "INCOME4_SPARSE_SINGLEWCHILDREN",
                        "INCOME4_SPARSE_COUPLE",
                        "INCOME4_SPARSE_COUPLEWCHILDREN",
                        "INCOME4_SPARSE_OTHER",
                        "INCOME4_SPARSE_OTHERWCHILDREN",
                        "INCOME5_DENSE_SINGLE",
                        "INCOME5_DENSE_SINGLEWCHILDREN",
                        "INCOME5_DENSE_COUPLE",
                        "INCOME5_DENSE_COUPLEWCHILDREN",
                        "INCOME5_DENSE_OTHER",
                        "INCOME5_DENSE_OTHERWCHILDREN",
                        "INCOME5_SPARSE_SINGLE",
                        "INCOME5_SPARSE_SINGLEWCHILDREN",
                        "INCOME5_SPARSE_COUPLE",
                        "INCOME5_SPARSE_COUPLEWCHILDREN",
                        "INCOME5_SPARSE_OTHER",
                        "INCOME5_SPARSE_OTHERWCHILDREN",
                        "REPRESENTATIVE_HOUSEHOLD",
                    ],
                },
                ["REGIONS_35_I!", "HOUSEHOLDS_I!"],
            ),
            lambda: xr.DataArray(
                0,
                {
                    "REGIONS_35_I!": [
                        "AUSTRIA",
                        "BELGIUM",
                        "BULGARIA",
                        "CROATIA",
                        "CYPRUS",
                        "CZECH_REPUBLIC",
                        "DENMARK",
                        "ESTONIA",
                        "FINLAND",
                        "FRANCE",
                        "GERMANY",
                        "GREECE",
                        "HUNGARY",
                        "IRELAND",
                        "ITALY",
                        "LATVIA",
                        "LITHUANIA",
                        "LUXEMBOURG",
                        "MALTA",
                        "NETHERLANDS",
                        "POLAND",
                        "PORTUGAL",
                        "ROMANIA",
                        "SLOVAKIA",
                        "SLOVENIA",
                        "SPAIN",
                        "SWEDEN",
                        "UK",
                        "CHINA",
                        "EASOC",
                        "INDIA",
                        "LATAM",
                        "RUSSIA",
                        "USMCA",
                        "LROW",
                    ],
                    "HOUSEHOLDS_I!": [
                        "INCOME1_DENSE_SINGLE",
                        "INCOME1_DENSE_SINGLEWCHILDREN",
                        "INCOME1_DENSE_COUPLE",
                        "INCOME1_DENSE_COUPLEWCHILDREN",
                        "INCOME1_DENSE_OTHER",
                        "INCOME1_DENSE_OTHERWCHILDREN",
                        "INCOME1_SPARSE_SINGLE",
                        "INCOME1_SPARSE_SINGLEWCHILDREN",
                        "INCOME1_SPARSE_COUPLE",
                        "INCOME1_SPARSE_COUPLEWCHILDREN",
                        "INCOME1_SPARSE_OTHER",
                        "INCOME1_SPARSE_OTHERWCHILDREN",
                        "INCOME2_DENSE_SINGLE",
                        "INCOME2_DENSE_SINGLEWCHILDREN",
                        "INCOME2_DENSE_COUPLE",
                        "INCOME2_DENSE_COUPLEWCHILDREN",
                        "INCOME2_DENSE_OTHER",
                        "INCOME2_DENSE_OTHERWCHILDREN",
                        "INCOME2_SPARSE_SINGLE",
                        "INCOME2_SPARSE_SINGLEWCHILDREN",
                        "INCOME2_SPARSE_COUPLE",
                        "INCOME2_SPARSE_COUPLEWCHILDREN",
                        "INCOME2_SPARSE_OTHER",
                        "INCOME2_SPARSE_OTHERWCHILDREN",
                        "INCOME3_DENSE_SINGLE",
                        "INCOME3_DENSE_SINGLEWCHILDREN",
                        "INCOME3_DENSE_COUPLE",
                        "INCOME3_DENSE_COUPLEWCHILDREN",
                        "INCOME3_DENSE_OTHER",
                        "INCOME3_DENSE_OTHERWCHILDREN",
                        "INCOME3_SPARSE_SINGLE",
                        "INCOME3_SPARSE_SINGLEWCHILDREN",
                        "INCOME3_SPARSE_COUPLE",
                        "INCOME3_SPARSE_COUPLEWCHILDREN",
                        "INCOME3_SPARSE_OTHER",
                        "INCOME3_SPARSE_OTHERWCHILDREN",
                        "INCOME4_DENSE_SINGLE",
                        "INCOME4_DENSE_SINGLEWCHILDREN",
                        "INCOME4_DENSE_COUPLE",
                        "INCOME4_DENSE_COUPLEWCHILDREN",
                        "INCOME4_DENSE_OTHER",
                        "INCOME4_DENSE_OTHERWCHILDREN",
                        "INCOME4_SPARSE_SINGLE",
                        "INCOME4_SPARSE_SINGLEWCHILDREN",
                        "INCOME4_SPARSE_COUPLE",
                        "INCOME4_SPARSE_COUPLEWCHILDREN",
                        "INCOME4_SPARSE_OTHER",
                        "INCOME4_SPARSE_OTHERWCHILDREN",
                        "INCOME5_DENSE_SINGLE",
                        "INCOME5_DENSE_SINGLEWCHILDREN",
                        "INCOME5_DENSE_COUPLE",
                        "INCOME5_DENSE_COUPLEWCHILDREN",
                        "INCOME5_DENSE_OTHER",
                        "INCOME5_DENSE_OTHERWCHILDREN",
                        "INCOME5_SPARSE_SINGLE",
                        "INCOME5_SPARSE_SINGLEWCHILDREN",
                        "INCOME5_SPARSE_COUPLE",
                        "INCOME5_SPARSE_COUPLEWCHILDREN",
                        "INCOME5_SPARSE_OTHER",
                        "INCOME5_SPARSE_OTHERWCHILDREN",
                        "REPRESENTATIVE_HOUSEHOLD",
                    ],
                },
                ["REGIONS_35_I!", "HOUSEHOLDS_I!"],
            ),
        ),
        dim=["REGIONS_35_I!", "HOUSEHOLDS_I!"],
    )


@component.add(
    name="check_households_financial_assets_negatives",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"households_financial_assets": 1},
)
def check_households_financial_assets_negatives():
    return sum(
        if_then_else(
            households_financial_assets().rename(
                {"REGIONS_35_I": "REGIONS_35_I!", "HOUSEHOLDS_I": "HOUSEHOLDS_I!"}
            )
            < 0,
            lambda: xr.DataArray(
                1,
                {
                    "REGIONS_35_I!": [
                        "AUSTRIA",
                        "BELGIUM",
                        "BULGARIA",
                        "CROATIA",
                        "CYPRUS",
                        "CZECH_REPUBLIC",
                        "DENMARK",
                        "ESTONIA",
                        "FINLAND",
                        "FRANCE",
                        "GERMANY",
                        "GREECE",
                        "HUNGARY",
                        "IRELAND",
                        "ITALY",
                        "LATVIA",
                        "LITHUANIA",
                        "LUXEMBOURG",
                        "MALTA",
                        "NETHERLANDS",
                        "POLAND",
                        "PORTUGAL",
                        "ROMANIA",
                        "SLOVAKIA",
                        "SLOVENIA",
                        "SPAIN",
                        "SWEDEN",
                        "UK",
                        "CHINA",
                        "EASOC",
                        "INDIA",
                        "LATAM",
                        "RUSSIA",
                        "USMCA",
                        "LROW",
                    ],
                    "HOUSEHOLDS_I!": [
                        "INCOME1_DENSE_SINGLE",
                        "INCOME1_DENSE_SINGLEWCHILDREN",
                        "INCOME1_DENSE_COUPLE",
                        "INCOME1_DENSE_COUPLEWCHILDREN",
                        "INCOME1_DENSE_OTHER",
                        "INCOME1_DENSE_OTHERWCHILDREN",
                        "INCOME1_SPARSE_SINGLE",
                        "INCOME1_SPARSE_SINGLEWCHILDREN",
                        "INCOME1_SPARSE_COUPLE",
                        "INCOME1_SPARSE_COUPLEWCHILDREN",
                        "INCOME1_SPARSE_OTHER",
                        "INCOME1_SPARSE_OTHERWCHILDREN",
                        "INCOME2_DENSE_SINGLE",
                        "INCOME2_DENSE_SINGLEWCHILDREN",
                        "INCOME2_DENSE_COUPLE",
                        "INCOME2_DENSE_COUPLEWCHILDREN",
                        "INCOME2_DENSE_OTHER",
                        "INCOME2_DENSE_OTHERWCHILDREN",
                        "INCOME2_SPARSE_SINGLE",
                        "INCOME2_SPARSE_SINGLEWCHILDREN",
                        "INCOME2_SPARSE_COUPLE",
                        "INCOME2_SPARSE_COUPLEWCHILDREN",
                        "INCOME2_SPARSE_OTHER",
                        "INCOME2_SPARSE_OTHERWCHILDREN",
                        "INCOME3_DENSE_SINGLE",
                        "INCOME3_DENSE_SINGLEWCHILDREN",
                        "INCOME3_DENSE_COUPLE",
                        "INCOME3_DENSE_COUPLEWCHILDREN",
                        "INCOME3_DENSE_OTHER",
                        "INCOME3_DENSE_OTHERWCHILDREN",
                        "INCOME3_SPARSE_SINGLE",
                        "INCOME3_SPARSE_SINGLEWCHILDREN",
                        "INCOME3_SPARSE_COUPLE",
                        "INCOME3_SPARSE_COUPLEWCHILDREN",
                        "INCOME3_SPARSE_OTHER",
                        "INCOME3_SPARSE_OTHERWCHILDREN",
                        "INCOME4_DENSE_SINGLE",
                        "INCOME4_DENSE_SINGLEWCHILDREN",
                        "INCOME4_DENSE_COUPLE",
                        "INCOME4_DENSE_COUPLEWCHILDREN",
                        "INCOME4_DENSE_OTHER",
                        "INCOME4_DENSE_OTHERWCHILDREN",
                        "INCOME4_SPARSE_SINGLE",
                        "INCOME4_SPARSE_SINGLEWCHILDREN",
                        "INCOME4_SPARSE_COUPLE",
                        "INCOME4_SPARSE_COUPLEWCHILDREN",
                        "INCOME4_SPARSE_OTHER",
                        "INCOME4_SPARSE_OTHERWCHILDREN",
                        "INCOME5_DENSE_SINGLE",
                        "INCOME5_DENSE_SINGLEWCHILDREN",
                        "INCOME5_DENSE_COUPLE",
                        "INCOME5_DENSE_COUPLEWCHILDREN",
                        "INCOME5_DENSE_OTHER",
                        "INCOME5_DENSE_OTHERWCHILDREN",
                        "INCOME5_SPARSE_SINGLE",
                        "INCOME5_SPARSE_SINGLEWCHILDREN",
                        "INCOME5_SPARSE_COUPLE",
                        "INCOME5_SPARSE_COUPLEWCHILDREN",
                        "INCOME5_SPARSE_OTHER",
                        "INCOME5_SPARSE_OTHERWCHILDREN",
                        "REPRESENTATIVE_HOUSEHOLD",
                    ],
                },
                ["REGIONS_35_I!", "HOUSEHOLDS_I!"],
            ),
            lambda: xr.DataArray(
                0,
                {
                    "REGIONS_35_I!": [
                        "AUSTRIA",
                        "BELGIUM",
                        "BULGARIA",
                        "CROATIA",
                        "CYPRUS",
                        "CZECH_REPUBLIC",
                        "DENMARK",
                        "ESTONIA",
                        "FINLAND",
                        "FRANCE",
                        "GERMANY",
                        "GREECE",
                        "HUNGARY",
                        "IRELAND",
                        "ITALY",
                        "LATVIA",
                        "LITHUANIA",
                        "LUXEMBOURG",
                        "MALTA",
                        "NETHERLANDS",
                        "POLAND",
                        "PORTUGAL",
                        "ROMANIA",
                        "SLOVAKIA",
                        "SLOVENIA",
                        "SPAIN",
                        "SWEDEN",
                        "UK",
                        "CHINA",
                        "EASOC",
                        "INDIA",
                        "LATAM",
                        "RUSSIA",
                        "USMCA",
                        "LROW",
                    ],
                    "HOUSEHOLDS_I!": [
                        "INCOME1_DENSE_SINGLE",
                        "INCOME1_DENSE_SINGLEWCHILDREN",
                        "INCOME1_DENSE_COUPLE",
                        "INCOME1_DENSE_COUPLEWCHILDREN",
                        "INCOME1_DENSE_OTHER",
                        "INCOME1_DENSE_OTHERWCHILDREN",
                        "INCOME1_SPARSE_SINGLE",
                        "INCOME1_SPARSE_SINGLEWCHILDREN",
                        "INCOME1_SPARSE_COUPLE",
                        "INCOME1_SPARSE_COUPLEWCHILDREN",
                        "INCOME1_SPARSE_OTHER",
                        "INCOME1_SPARSE_OTHERWCHILDREN",
                        "INCOME2_DENSE_SINGLE",
                        "INCOME2_DENSE_SINGLEWCHILDREN",
                        "INCOME2_DENSE_COUPLE",
                        "INCOME2_DENSE_COUPLEWCHILDREN",
                        "INCOME2_DENSE_OTHER",
                        "INCOME2_DENSE_OTHERWCHILDREN",
                        "INCOME2_SPARSE_SINGLE",
                        "INCOME2_SPARSE_SINGLEWCHILDREN",
                        "INCOME2_SPARSE_COUPLE",
                        "INCOME2_SPARSE_COUPLEWCHILDREN",
                        "INCOME2_SPARSE_OTHER",
                        "INCOME2_SPARSE_OTHERWCHILDREN",
                        "INCOME3_DENSE_SINGLE",
                        "INCOME3_DENSE_SINGLEWCHILDREN",
                        "INCOME3_DENSE_COUPLE",
                        "INCOME3_DENSE_COUPLEWCHILDREN",
                        "INCOME3_DENSE_OTHER",
                        "INCOME3_DENSE_OTHERWCHILDREN",
                        "INCOME3_SPARSE_SINGLE",
                        "INCOME3_SPARSE_SINGLEWCHILDREN",
                        "INCOME3_SPARSE_COUPLE",
                        "INCOME3_SPARSE_COUPLEWCHILDREN",
                        "INCOME3_SPARSE_OTHER",
                        "INCOME3_SPARSE_OTHERWCHILDREN",
                        "INCOME4_DENSE_SINGLE",
                        "INCOME4_DENSE_SINGLEWCHILDREN",
                        "INCOME4_DENSE_COUPLE",
                        "INCOME4_DENSE_COUPLEWCHILDREN",
                        "INCOME4_DENSE_OTHER",
                        "INCOME4_DENSE_OTHERWCHILDREN",
                        "INCOME4_SPARSE_SINGLE",
                        "INCOME4_SPARSE_SINGLEWCHILDREN",
                        "INCOME4_SPARSE_COUPLE",
                        "INCOME4_SPARSE_COUPLEWCHILDREN",
                        "INCOME4_SPARSE_OTHER",
                        "INCOME4_SPARSE_OTHERWCHILDREN",
                        "INCOME5_DENSE_SINGLE",
                        "INCOME5_DENSE_SINGLEWCHILDREN",
                        "INCOME5_DENSE_COUPLE",
                        "INCOME5_DENSE_COUPLEWCHILDREN",
                        "INCOME5_DENSE_OTHER",
                        "INCOME5_DENSE_OTHERWCHILDREN",
                        "INCOME5_SPARSE_SINGLE",
                        "INCOME5_SPARSE_SINGLEWCHILDREN",
                        "INCOME5_SPARSE_COUPLE",
                        "INCOME5_SPARSE_COUPLEWCHILDREN",
                        "INCOME5_SPARSE_OTHER",
                        "INCOME5_SPARSE_OTHERWCHILDREN",
                        "REPRESENTATIVE_HOUSEHOLD",
                    ],
                },
                ["REGIONS_35_I!", "HOUSEHOLDS_I!"],
            ),
        ),
        dim=["REGIONS_35_I!", "HOUSEHOLDS_I!"],
    )


@component.add(
    name="check_households_liabilities_negatives",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"households_financial_liabilities": 1},
)
def check_households_liabilities_negatives():
    return sum(
        if_then_else(
            households_financial_liabilities().rename(
                {"REGIONS_35_I": "REGIONS_35_I!", "HOUSEHOLDS_I": "HOUSEHOLDS_I!"}
            )
            < 0,
            lambda: xr.DataArray(
                1,
                {
                    "REGIONS_35_I!": [
                        "AUSTRIA",
                        "BELGIUM",
                        "BULGARIA",
                        "CROATIA",
                        "CYPRUS",
                        "CZECH_REPUBLIC",
                        "DENMARK",
                        "ESTONIA",
                        "FINLAND",
                        "FRANCE",
                        "GERMANY",
                        "GREECE",
                        "HUNGARY",
                        "IRELAND",
                        "ITALY",
                        "LATVIA",
                        "LITHUANIA",
                        "LUXEMBOURG",
                        "MALTA",
                        "NETHERLANDS",
                        "POLAND",
                        "PORTUGAL",
                        "ROMANIA",
                        "SLOVAKIA",
                        "SLOVENIA",
                        "SPAIN",
                        "SWEDEN",
                        "UK",
                        "CHINA",
                        "EASOC",
                        "INDIA",
                        "LATAM",
                        "RUSSIA",
                        "USMCA",
                        "LROW",
                    ],
                    "HOUSEHOLDS_I!": [
                        "INCOME1_DENSE_SINGLE",
                        "INCOME1_DENSE_SINGLEWCHILDREN",
                        "INCOME1_DENSE_COUPLE",
                        "INCOME1_DENSE_COUPLEWCHILDREN",
                        "INCOME1_DENSE_OTHER",
                        "INCOME1_DENSE_OTHERWCHILDREN",
                        "INCOME1_SPARSE_SINGLE",
                        "INCOME1_SPARSE_SINGLEWCHILDREN",
                        "INCOME1_SPARSE_COUPLE",
                        "INCOME1_SPARSE_COUPLEWCHILDREN",
                        "INCOME1_SPARSE_OTHER",
                        "INCOME1_SPARSE_OTHERWCHILDREN",
                        "INCOME2_DENSE_SINGLE",
                        "INCOME2_DENSE_SINGLEWCHILDREN",
                        "INCOME2_DENSE_COUPLE",
                        "INCOME2_DENSE_COUPLEWCHILDREN",
                        "INCOME2_DENSE_OTHER",
                        "INCOME2_DENSE_OTHERWCHILDREN",
                        "INCOME2_SPARSE_SINGLE",
                        "INCOME2_SPARSE_SINGLEWCHILDREN",
                        "INCOME2_SPARSE_COUPLE",
                        "INCOME2_SPARSE_COUPLEWCHILDREN",
                        "INCOME2_SPARSE_OTHER",
                        "INCOME2_SPARSE_OTHERWCHILDREN",
                        "INCOME3_DENSE_SINGLE",
                        "INCOME3_DENSE_SINGLEWCHILDREN",
                        "INCOME3_DENSE_COUPLE",
                        "INCOME3_DENSE_COUPLEWCHILDREN",
                        "INCOME3_DENSE_OTHER",
                        "INCOME3_DENSE_OTHERWCHILDREN",
                        "INCOME3_SPARSE_SINGLE",
                        "INCOME3_SPARSE_SINGLEWCHILDREN",
                        "INCOME3_SPARSE_COUPLE",
                        "INCOME3_SPARSE_COUPLEWCHILDREN",
                        "INCOME3_SPARSE_OTHER",
                        "INCOME3_SPARSE_OTHERWCHILDREN",
                        "INCOME4_DENSE_SINGLE",
                        "INCOME4_DENSE_SINGLEWCHILDREN",
                        "INCOME4_DENSE_COUPLE",
                        "INCOME4_DENSE_COUPLEWCHILDREN",
                        "INCOME4_DENSE_OTHER",
                        "INCOME4_DENSE_OTHERWCHILDREN",
                        "INCOME4_SPARSE_SINGLE",
                        "INCOME4_SPARSE_SINGLEWCHILDREN",
                        "INCOME4_SPARSE_COUPLE",
                        "INCOME4_SPARSE_COUPLEWCHILDREN",
                        "INCOME4_SPARSE_OTHER",
                        "INCOME4_SPARSE_OTHERWCHILDREN",
                        "INCOME5_DENSE_SINGLE",
                        "INCOME5_DENSE_SINGLEWCHILDREN",
                        "INCOME5_DENSE_COUPLE",
                        "INCOME5_DENSE_COUPLEWCHILDREN",
                        "INCOME5_DENSE_OTHER",
                        "INCOME5_DENSE_OTHERWCHILDREN",
                        "INCOME5_SPARSE_SINGLE",
                        "INCOME5_SPARSE_SINGLEWCHILDREN",
                        "INCOME5_SPARSE_COUPLE",
                        "INCOME5_SPARSE_COUPLEWCHILDREN",
                        "INCOME5_SPARSE_OTHER",
                        "INCOME5_SPARSE_OTHERWCHILDREN",
                        "REPRESENTATIVE_HOUSEHOLD",
                    ],
                },
                ["REGIONS_35_I!", "HOUSEHOLDS_I!"],
            ),
            lambda: xr.DataArray(
                0,
                {
                    "REGIONS_35_I!": [
                        "AUSTRIA",
                        "BELGIUM",
                        "BULGARIA",
                        "CROATIA",
                        "CYPRUS",
                        "CZECH_REPUBLIC",
                        "DENMARK",
                        "ESTONIA",
                        "FINLAND",
                        "FRANCE",
                        "GERMANY",
                        "GREECE",
                        "HUNGARY",
                        "IRELAND",
                        "ITALY",
                        "LATVIA",
                        "LITHUANIA",
                        "LUXEMBOURG",
                        "MALTA",
                        "NETHERLANDS",
                        "POLAND",
                        "PORTUGAL",
                        "ROMANIA",
                        "SLOVAKIA",
                        "SLOVENIA",
                        "SPAIN",
                        "SWEDEN",
                        "UK",
                        "CHINA",
                        "EASOC",
                        "INDIA",
                        "LATAM",
                        "RUSSIA",
                        "USMCA",
                        "LROW",
                    ],
                    "HOUSEHOLDS_I!": [
                        "INCOME1_DENSE_SINGLE",
                        "INCOME1_DENSE_SINGLEWCHILDREN",
                        "INCOME1_DENSE_COUPLE",
                        "INCOME1_DENSE_COUPLEWCHILDREN",
                        "INCOME1_DENSE_OTHER",
                        "INCOME1_DENSE_OTHERWCHILDREN",
                        "INCOME1_SPARSE_SINGLE",
                        "INCOME1_SPARSE_SINGLEWCHILDREN",
                        "INCOME1_SPARSE_COUPLE",
                        "INCOME1_SPARSE_COUPLEWCHILDREN",
                        "INCOME1_SPARSE_OTHER",
                        "INCOME1_SPARSE_OTHERWCHILDREN",
                        "INCOME2_DENSE_SINGLE",
                        "INCOME2_DENSE_SINGLEWCHILDREN",
                        "INCOME2_DENSE_COUPLE",
                        "INCOME2_DENSE_COUPLEWCHILDREN",
                        "INCOME2_DENSE_OTHER",
                        "INCOME2_DENSE_OTHERWCHILDREN",
                        "INCOME2_SPARSE_SINGLE",
                        "INCOME2_SPARSE_SINGLEWCHILDREN",
                        "INCOME2_SPARSE_COUPLE",
                        "INCOME2_SPARSE_COUPLEWCHILDREN",
                        "INCOME2_SPARSE_OTHER",
                        "INCOME2_SPARSE_OTHERWCHILDREN",
                        "INCOME3_DENSE_SINGLE",
                        "INCOME3_DENSE_SINGLEWCHILDREN",
                        "INCOME3_DENSE_COUPLE",
                        "INCOME3_DENSE_COUPLEWCHILDREN",
                        "INCOME3_DENSE_OTHER",
                        "INCOME3_DENSE_OTHERWCHILDREN",
                        "INCOME3_SPARSE_SINGLE",
                        "INCOME3_SPARSE_SINGLEWCHILDREN",
                        "INCOME3_SPARSE_COUPLE",
                        "INCOME3_SPARSE_COUPLEWCHILDREN",
                        "INCOME3_SPARSE_OTHER",
                        "INCOME3_SPARSE_OTHERWCHILDREN",
                        "INCOME4_DENSE_SINGLE",
                        "INCOME4_DENSE_SINGLEWCHILDREN",
                        "INCOME4_DENSE_COUPLE",
                        "INCOME4_DENSE_COUPLEWCHILDREN",
                        "INCOME4_DENSE_OTHER",
                        "INCOME4_DENSE_OTHERWCHILDREN",
                        "INCOME4_SPARSE_SINGLE",
                        "INCOME4_SPARSE_SINGLEWCHILDREN",
                        "INCOME4_SPARSE_COUPLE",
                        "INCOME4_SPARSE_COUPLEWCHILDREN",
                        "INCOME4_SPARSE_OTHER",
                        "INCOME4_SPARSE_OTHERWCHILDREN",
                        "INCOME5_DENSE_SINGLE",
                        "INCOME5_DENSE_SINGLEWCHILDREN",
                        "INCOME5_DENSE_COUPLE",
                        "INCOME5_DENSE_COUPLEWCHILDREN",
                        "INCOME5_DENSE_OTHER",
                        "INCOME5_DENSE_OTHERWCHILDREN",
                        "INCOME5_SPARSE_SINGLE",
                        "INCOME5_SPARSE_SINGLEWCHILDREN",
                        "INCOME5_SPARSE_COUPLE",
                        "INCOME5_SPARSE_COUPLEWCHILDREN",
                        "INCOME5_SPARSE_OTHER",
                        "INCOME5_SPARSE_OTHERWCHILDREN",
                        "REPRESENTATIVE_HOUSEHOLD",
                    ],
                },
                ["REGIONS_35_I!", "HOUSEHOLDS_I!"],
            ),
        ),
        dim=["REGIONS_35_I!", "HOUSEHOLDS_I!"],
    )


@component.add(
    name="check_ratio_liabilities_to_assets",
    subscripts=["REGIONS_35_I", "HOUSEHOLDS_I"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "households_financial_liabilities": 1,
        "households_financial_assets": 1,
        "households_capital_stock": 1,
    },
)
def check_ratio_liabilities_to_assets():
    return zidz(
        households_financial_liabilities(),
        households_capital_stock() + households_financial_assets(),
    )


@component.add(
    name="ratio_liabilities_to_assets",
    subscripts=["REGIONS_35_I", "HOUSEHOLDS_I"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_households_financial_liabilities": 1,
        "initial_households_capital_stock": 1,
        "initial_households_financial_assets": 1,
    },
)
def ratio_liabilities_to_assets():
    """
    Ratio of liabilites to total assets
    """
    return zidz(
        initial_households_financial_liabilities(),
        initial_households_capital_stock() + initial_households_financial_assets(),
    )
