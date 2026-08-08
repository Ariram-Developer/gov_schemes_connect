import mysql.connector

# ==========================================
# 1. DATABASE CREDENTIALS (No password for local root)
# ==========================================
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'database': 'gov_scheme_connect' # Exact match to your schema.sql
}

# ==========================================
# 2. MASTER SCHEMES ROSTER
# ==========================================
schemes_data = [
    # --- 1. UNEDUCATED ---
    {
        "title": "Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGS)",
        "category": "Uneducated",
        "description": "Provides up to 100 days of guaranteed wage employment per year to enhance livelihood security in rural areas for unskilled labor.",
        "eligibility_criteria": "Indian citizen, 18 years or above, residing in a rural household.",
        "required_documents": "Aadhaar Card, Ration Card, Job Card, Bank Passbook, Passport-size Photo"
    },
    {
        "title": "Pradhan Mantri Kaushal Vikas Yojana (PMKVY)",
        "category": "Uneducated",
        "description": "Free skill training, certification, and improved employment opportunities for youth and dropouts.",
        "eligibility_criteria": "Indian citizen, unemployed youth, school/college dropouts, aged 18-45 years.",
        "required_documents": "Aadhaar Card, Educational Certificates, Bank Passbook, Passport-size Photo"
    },
    {
        "title": "Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)",
        "category": "Uneducated",
        "description": "Free skill training with job placement assistance for rural youth from poor families.",
        "eligibility_criteria": "Rural youth aged 15-35 years from poor families.",
        "required_documents": "Aadhaar Card, Ration Card, Income Certificate, Bank Passbook"
    },

    # --- 2. UNEMPLOYMENT ---
    {
        "title": "PM Internship Scheme",
        "category": "Unemployment",
        "description": "Provides internship opportunities with monthly financial support and practical work experience.",
        "eligibility_criteria": "Eligible young graduates/diploma holders as per scheme guidelines.",
        "required_documents": "Aadhaar Card, Educational Certificates, Bank Passbook, Passport-size Photo"
    },
    {
        "title": "National Career Service (NCS)",
        "category": "Unemployment",
        "description": "Free job portal providing career guidance and employment opportunities.",
        "eligibility_criteria": "Any Indian job seeker or employer.",
        "required_documents": "Aadhaar Card, Educational Certificates, Resume, Mobile Number, Email ID"
    },
    {
        "title": "Naan Mudhalvan (Tamil Nadu)",
        "category": "Unemployment",
        "description": "Massive skill development and career guidance initiative for students and youth to provide placement support.",
        "eligibility_criteria": "Students and youth studying or residing in Tamil Nadu.",
        "required_documents": "Aadhaar Card, Student ID, Educational Certificates"
    },

    # --- 3. SHELTER ---
    {
        "title": "Pradhan Mantri Awas Yojana - Urban (PMAY-U)",
        "category": "Shelter",
        "description": "Financial assistance and interest subsidy to buy or build a permanent house with basic amenities.",
        "eligibility_criteria": "Indian citizen, EWS/LIG/MIG family, should not own a pucca house anywhere in India.",
        "required_documents": "Aadhaar Card, Income Certificate, Address Proof, Bank Passbook"
    },
    {
        "title": "Kalaignar Kanavu Illam Scheme (Tamil Nadu)",
        "category": "Shelter",
        "description": "Financial assistance to construct a concrete house for eligible rural families.",
        "eligibility_criteria": "Eligible rural families living in huts or unsafe houses, selected by State Government.",
        "required_documents": "Aadhaar Card, Family Ration Card, Income Certificate, Patta Land Documents, Bank Passbook"
    },
    {
        "title": "Affordable Rental Housing (ARH)",
        "category": "Shelter",
        "description": "Affordable rental accommodation in urban areas for migrant workers.",
        "eligibility_criteria": "Urban migrants, economically weaker sections, low-income workers, students.",
        "required_documents": "Aadhaar Card, Identity Proof, Income Proof"
    },

    # --- 4. SMALL BUSINESS ---
    {
        "title": "Pradhan Mantri Mudra Yojana (PMMY)",
        "category": "Small Business",
        "description": "Collateral-free business loans up to ₹20 lakh for non-corporate small businesses.",
        "eligibility_criteria": "Indian citizen, small business owner, startup, or self-employed person.",
        "required_documents": "Aadhaar Card, PAN Card, Business Proof, Bank Passbook"
    },
    {
        "title": "Prime Minister Employment Generation Programme (PMEGP)",
        "category": "Small Business",
        "description": "Subsidized bank loan to start a new business or micro-enterprise.",
        "eligibility_criteria": "Indian citizen above 18 years; minimum VIII standard required for larger projects.",
        "required_documents": "Aadhaar Card, PAN Card, Project Report, Educational Certificate, Bank Passbook"
    },
    {
        "title": "Stand-Up India Scheme",
        "category": "Small Business",
        "description": "Bank loans from ₹10 lakh to ₹1 crore for greenfield enterprises.",
        "eligibility_criteria": "SC/ST entrepreneurs and women entrepreneurs aged 18 years and above.",
        "required_documents": "Aadhaar Card, PAN Card, Business Plan, Bank Details"
    },

    # --- 5. PENSION ---
    {
        "title": "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
        "category": "Pension",
        "description": "Monthly pension assistance for senior citizens.",
        "eligibility_criteria": "Senior citizens aged 60 years and above belonging to eligible low-income families.",
        "required_documents": "Aadhaar Card, Age Proof, Income Certificate, Bank Passbook"
    },
    {
        "title": "Atal Pension Yojana (APY)",
        "category": "Pension",
        "description": "Guaranteed monthly pension after the age of 60 years based on contributions.",
        "eligibility_criteria": "Indian citizens aged 18-40 years with a savings bank account.",
        "required_documents": "Aadhaar Card, Bank Passbook, Mobile Number"
    },
    {
        "title": "Destitute Widow Pension Scheme (Tamil Nadu)",
        "category": "Pension",
        "description": "Monthly financial assistance for destitute widows.",
        "eligibility_criteria": "Destitute widows meeting the state's eligibility criteria.",
        "required_documents": "Aadhaar Card, Husbands Death Certificate, Income Certificate, Bank Passbook"
    },

    # --- 6. HEALTH ---
    {
        "title": "Ayushman Bharat - PM-JAY",
        "category": "Health",
        "description": "Cashless treatment up to the scheme limit at empanelled hospitals.",
        "eligibility_criteria": "Eligible low-income families as per scheme guidelines.",
        "required_documents": "Aadhaar Card, Ration Card, Mobile Number"
    },
    {
        "title": "Chief Minister's Comprehensive Health Insurance Scheme (CMCHIS)",
        "category": "Health",
        "description": "Cashless treatment in government and empanelled private hospitals in TN.",
        "eligibility_criteria": "Eligible Tamil Nadu families meeting the prescribed income criteria.",
        "required_documents": "Aadhaar Card, Family Ration Card, Income Certificate"
    },

    # --- 7. FARMERS ---
    {
        "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "category": "Farmers",
        "description": "₹6,000 per year provided in three installments to farmer families.",
        "eligibility_criteria": "Indian farmer owning eligible cultivable land.",
        "required_documents": "Aadhaar Card, Land Records, Bank Passbook, Mobile Number"
    }
]

def seed_database():
    try:
        print("Connecting to database...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Step 1: Find an Admin to assign these schemes to
        cursor.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
        admin = cursor.fetchone()
        
        if not admin:
            print("❌ ERROR: No Admin account found in your database!")
            print("Please run your app, register a new account, manually change its role to 'admin' in MySQL, and then run this script again.")
            return

        admin_id = admin[0]
        print(f"✅ Found Admin (User ID: {admin_id}). Injecting {len(schemes_data)} schemes...")

        # Step 2: Insert the schemes
        insert_query = """
            INSERT INTO schemes (title, category, description, eligibility_criteria, required_documents, created_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        success_count = 0
        for scheme in schemes_data:
            values = (
                scheme['title'], 
                scheme['category'], 
                scheme['description'], 
                scheme['eligibility_criteria'], 
                scheme['required_documents'],
                admin_id # <-- The crucial missing link!
            )
            cursor.execute(insert_query, values)
            success_count += 1

        conn.commit()
        print(f"✅ Success! {success_count} schemes across 7 categories have been seeded into your database.")
        print("Go to your Citizen Portal to see the beautifully populated grid!")

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    seed_database()