import pandas as pd

# ==========================================================
# DATABASE LOADER
# ==========================================================

DATABASE = {
    "materials": pd.read_csv("database/materials.csv"),
    "joints": pd.read_csv("database/joint_types.csv"),
    "heads": pd.read_csv("database/head_types.csv"),
    "supports": pd.read_csv("database/support_types.csv"),
    "electrodes": pd.read_csv("database/electrodes.csv"),
    "welding": pd.read_csv("database/welding_parameters.csv"),
    "distortion": pd.read_csv("database/distortion_rules.csv"),
    "inspection": pd.read_csv("database/inspection_methods.csv"),
    "pwht": pd.read_csv("database/heat_treatment.csv"),
    "shielding": pd.read_csv("database/shielding_gases.csv"),
    "recommendation": pd.read_csv("database/recommendations.csv"),
}

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def _find_exact(df, column, value):
    """
    Returns the first matching row as dictionary.
    """

    row = df[df[column] == value]

    if row.empty:
        return None

    return row.iloc[0].to_dict()


def _find_range(df, min_col, max_col, value):
    """
    Returns row where value lies between min and max.
    """

    row = df[
        (df[min_col] <= value) &
        (df[max_col] >= value)
    ]

    if row.empty:
        return None

    return row.iloc[0].to_dict()


# ==========================================================
# VALIDATION
# ==========================================================

def validate_material(material):

    return material in DATABASE["materials"]["Material"].values


def validate_joint(joint):

    return joint in DATABASE["joints"]["Joint_Type"].values


def validate_support(support):

    return support in DATABASE["supports"]["Support_Type"].values


def validate_thickness(thickness):

    return thickness > 0


# ==========================================================
# MATERIAL DATABASE
# ==========================================================

def get_material(material):

    return _find_exact(
        DATABASE["materials"],
        "Material",
        material
    )


# ==========================================================
# JOINT DATABASE
# ==========================================================

def get_joint(joint):

    return _find_exact(
        DATABASE["joints"],
        "Joint_Type",
        joint
    )


# ==========================================================
# HEAD TYPE DATABASE
# ==========================================================

def get_head(head):

    return _find_exact(
        DATABASE["heads"],
        "Head_Type",
        head
    )


# ==========================================================
# SUPPORT DATABASE
# ==========================================================

def get_support(support):

    return _find_exact(
        DATABASE["supports"],
        "Support_Type",
        support
    )


# ==========================================================
# ELECTRODE DATABASE
# ==========================================================

def get_electrode(material):

    return _find_exact(
        DATABASE["electrodes"],
        "Material",
        material
    )
    # ==========================================================
# WELDING DATABASE
# ==========================================================

def get_welding(material, thickness):

    # -----------------------------
    # Clean the inputs
    # -----------------------------
    material = str(material).strip()
    thickness = float(thickness)

    df = DATABASE["welding"].copy()

    # -----------------------------
    # Clean dataframe
    # -----------------------------
    df["Material"] = (
        df["Material"]
        .astype(str)
        .str.strip()
    )

    df["Min_Thickness"] = pd.to_numeric(
        df["Min_Thickness"],
        errors="coerce"
    )

    df["Max_Thickness"] = pd.to_numeric(
        df["Max_Thickness"],
        errors="coerce"
    )

    # -----------------------------
    # Find match
    # -----------------------------
    row = df[
        (df["Material"].str.lower() == material.lower()) &
        (df["Min_Thickness"] <= thickness) &
        (df["Max_Thickness"] >= thickness)
    ]

    # -----------------------------
    # If nothing found
    # -----------------------------
    if row.empty:

        print("Material:", material)
        print("Thickness:", thickness)

        print(df)

        return None

    return row.iloc[0].to_dict()


# ==========================================================
# DISTORTION DATABASE
# ==========================================================

def get_distortion(thickness):

    return _find_range(
        DATABASE["distortion"],
        "Thickness_Min",
        "Thickness_Max",
        thickness
    )


# ==========================================================
# INSPECTION DATABASE
# ==========================================================

def get_inspection(material):

    return _find_exact(
        DATABASE["inspection"],
        "Material",
        material
    )


# ==========================================================
# PWHT DATABASE
# ==========================================================

def get_heat_treatment(material, thickness):

    df = DATABASE["pwht"]

    row = df[
        (df["Material"] == material) &
        (df["Min_Thickness"] <= thickness) &
        (df["Max_Thickness"] >= thickness)
    ]

    if row.empty:
        return None

    return row.iloc[0].to_dict()


# ==========================================================
# SHIELDING GAS DATABASE
# ==========================================================

def get_shielding_gas(process):

    return _find_exact(
        DATABASE["shielding"],
        "Process",
        process
    )


# ==========================================================
# RECOMMENDATION DATABASE
# ==========================================================

def get_recommendation(risk):

    return _find_exact(
        DATABASE["recommendation"],
        "Risk",
        risk
    )


# ==========================================================
# COMPLETE ENGINE
# ==========================================================

def get_complete_recommendation(material, thickness, joint, support):
    """
    Returns all engineering recommendations in one dictionary.
    """

    welding = get_welding(material, thickness)

    process = welding["Process"] if welding else None

    return {
        "material": get_material(material),
        "joint": get_joint(joint),
        "support": get_support(support),
        "electrode": get_electrode(material),
        "welding": welding,
        "distortion": get_distortion(thickness),
        "inspection": get_inspection(material),
        "pwht": get_heat_treatment(material, thickness),
        "shielding_gas": get_shielding_gas(process) if process else None,
        "recommendation": get_recommendation(
            get_distortion(thickness)["Risk"]
        ) if get_distortion(thickness) else None
    }