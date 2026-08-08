import mysql.connector

# ==========================================
# 1. UPDATE YOUR DATABASE CREDENTIALS HERE
# ==========================================
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', # Left empty for your local setup
    'database': 'gov_schemes_db'
}

# ==========================================
# 2. MASTER SCHEMES ROSTER (Extracted from Images)
# ==========================================
schemes_data = [
    
    # --- 1. UNEDUCATED (Focus on unskilled labor & dropouts) ---
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
        "required_documents": "Aadhaar Card, Educational Certificates (if available), Bank Passbook, Passport-size Photo"
    },
    {
        "title": "Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)",
        "category": "Uneducated",
        "description": "Free skill training with job placement assistance for rural youth from poor families.",
        "eligibility_criteria": "Rural youth aged 15-35 years from poor families.",
        "required_documents": "Aadhaar Card, Ration Card, Income Certificate, Bank Passbook"
    },

    # --- 2. UNEMPLOYMENT (Focus on job seekers & internships) ---
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
        "required_documents": "Aadhaar Card, Family Ration Card, Income Certificate, Patta/Land Documents, Bank Passbook"
    },
    {
        "title": "Affordable Rental Housing (ARH)",
        "category": "Shelter",
        "description": "Affordable rental accommodation in urban areas for migrant workers.",
        "eligibility_criteria": "Urban migrants, economically weaker sections, low-income workers, students.",
        "required_documents": "Aadhaar Card, Identity Proof, Income Proof (if required)"
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
        "required_documents": "Aadhaar Card, Husband's Death Certificate, Income Certificate, Bank Passbook"
    },

    # --- 6. HEALTH ---
    {
        "title": "Ayushman Bharat - PM-JAY",
        "category": "Health",
        "description": "Cashless treatment up to the scheme limit at empanelled hospitals.",
        "eligibility_criteria": "Eligible low-income families as per scheme guidelines.",
        "required_documents": "Aadhaar Card, Ration Card/Family ID, Mobile Number"
    },
    {
        "title": "Chief Minister's Comprehensive Health Insurance Scheme (CMCHIS)",
        "category": "Health",
        "description": "Cashless treatment in government and empanelled private hospitals in TN.",
        "eligibility_criteria": "Eligible Tamil Nadu families meeting the prescribed income criteria.",
        "required_documents": "Aadhaar Card, Family Ration Card, Income Certificate"
    },
    {
        "title": "Janani Suraksha Yojana (JSY)",
        "category": "Health",
        "description": "Financial assistance for institutional delivery to reduce maternal mortality.",
        "eligibility_criteria": "Pregnant women, especially from eligible low-income families.",
        "required_documents": "Aadhaar Card, Pregnancy Registration, Bank Passbook"
    },

    # --- 7. FARMERS ---
    {
        "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "category": "Farmers",
        "description": "₹6,000 per year provided in three installments to farmer families.",
        "eligibility_criteria": "Indian farmer owning eligible cultivable land.",
        "required_documents": "Aadhaar Card, Land Records, Bank Passbook, Mobile Number"
    },
    {
        "title": "Kisan Credit Card (KCC)",
        "category": "Farmers",
        "description": "Low-interest agricultural loans for farming needs.",
        "eligibility_criteria": "Farmers involved in agriculture, animal husbandry, or fisheries.",
        "required_documents": "Aadhaar Card, Land Records, Passport-size Photo, Bank Passbook"
    },
    {
        "title": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "category": "Farmers",
        "description": "Crop insurance against natural calamities, pests, and diseases.",
        "eligibility_criteria": "Farmers cultivating notified crops.",
        "required_documents": "Aadhaar Card, Land Records, Bank Passbook, Crop Sowing Certificate"
    },

    # --- 8. SCHOLARSHIP ---
    {
        "title": "AICTE Saksham Scholarship - Differently Abled Students",
        "category": "Scholarship",
        "description": "Financial assistance of up to ₹30,000 for technical education, books, and equipment.",
        "eligibility_criteria": "Student with more than 40% disability studying eligible Diploma/Degree in AICTE-approved institution.",
        "required_documents": "Disability Certificate, 10th/12th Marksheet, Income Certificate, Admission Letter, Aadhaar"
    },
    {
        "title": "AICTE Swanath Scholarship",
        "category": "Scholarship",
        "description": "Financial assistance for continuing technical education and meeting educational expenses.",
        "eligibility_criteria": "Eligible orphan students, children of parents who died due to COVID-19, or wards of Armed Forces martyred in action.",
        "required_documents": "Death/Martyr Certificate, Income Certificate, Marksheets, Bonafide Certificate, Aadhaar"
    },
    {
        "title": "AICTE Pragati Scholarship - Girls",
        "category": "Scholarship",
        "description": "Tuition fee support up to ₹30,000 and ₹2,000/month incidentals to encourage technical education for girls.",
        "eligibility_criteria": "Girl student studying Diploma/Degree in AICTE-approved institution within prescribed family income limit.",
        "required_documents": "10th/12th Marksheet, Income Certificate, Admission Letter, Tuition Fee Receipt, Aadhaar"
    },
    {
        "title": "AICTE PG Scholarship - GATE/GPAT",
        "category": "Scholarship",
        "description": "Monthly financial assistance during the eligible PG period to encourage higher technical education.",
        "eligibility_criteria": "GATE/GPAT-qualified student admitted to eligible full-time PG programme.",
        "required_documents": "GATE/GPAT Scorecard, PG Admission Proof, Degree Certificates, Aadhaar, Bank Details"
    },
    {
        "title": "AICTE National Doctoral Fellowship (NDF)",
        "category": "Scholarship",
        "description": "Fellowship and financial support for doctoral research and innovation activities.",
        "eligibility_criteria": "Eligible full-time PhD/research scholars satisfying AICTE academic and GATE requirements.",
        "required_documents": "PhD Admission Certificate, Degree Certificates, Marksheets, GATE Scorecard, ID Proof"
    },

    # --- 9. AUTISM SUPPORT ---
    {
        "title": "Niramaya Health Insurance Scheme",
        "category": "Autism Support",
        "description": "Health insurance for children with autism covering therapy, medicines, hospitalization, and treatment.",
        "eligibility_criteria": "Child with Autism and valid disability certificate/UDID.",
        "required_documents": "Child Aadhaar, Parent Aadhaar, Disability Certificate, UDID Card, Medical Reports"
    },
    {
        "title": "Disha Scheme",
        "category": "Autism Support",
        "description": "Early intervention, therapy, education, and skill development for children.",
        "eligibility_criteria": "Autism child aged 0–10 years.",
        "required_documents": "Child Aadhaar, Parent Aadhaar, Birth Certificate, Disability Certificate, UDID Card"
    },
    {
        "title": "Vikaas Scheme",
        "category": "Autism Support",
        "description": "Day care, therapy, education, vocational training, and independent living skills.",
        "eligibility_criteria": "Autism child aged 10 years and above.",
        "required_documents": "Child Aadhaar, Parent Aadhaar, Disability Certificate, UDID Card, Income Certificate"
    },
    {
        "title": "Samarth Scheme",
        "category": "Autism Support",
        "description": "Residential care and respite care for children with disabilities requiring intensive support.",
        "eligibility_criteria": "Child with Autism requiring residential support.",
        "required_documents": "Child Aadhaar, Parent Aadhaar, Disability Certificate, UDID Card, Medical Reports"
    },
    {
        "title": "Gharaunda Scheme",
        "category": "Autism Support",
        "description": "Long-term residential care and independent living support for adults with autism.",
        "eligibility_criteria": "Adults with Autism (18+ years).",
        "required_documents": "Aadhaar Card, Disability Certificate, UDID Card, Medical Reports, Address Proof"
    },
    {
        "title": "UDID Card Scheme",
        "category": "Autism Support",
        "description": "Provides a Unique Disability ID to easily access all government benefits and schemes.",
        "eligibility_criteria": "Person diagnosed with Autism Spectrum Disorder (or other recognized disabilities).",
        "required_documents": "Aadhaar Card, Disability Certificate, Passport Photo, Address Proof, Mobile Number"
    }
]

def seed_database():
    try:
        print("Connecting to database...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        print(f"Successfully connected! Injecting {len(schemes_data)} schemes...")

        # We use INSERT IGNORE to prevent duplicate entries if you run this multiple times
        insert_query = """
            INSERT IGNORE INTO schemes (title, category, description, eligibility_criteria, required_documents)
            VALUES (%s, %s, %s, %s, %s)
        """

        success_count = 0
        for scheme in schemes_data:
            values = (
                scheme['title'], 
                scheme['category'], 
                scheme['description'], 
                scheme['eligibility_criteria'], 
                scheme['required_documents']
            )
            cursor.execute(insert_query, values)
            # Only count if a new row was actually inserted
            if cursor.rowcount > 0:
                success_count += 1

        conn.commit()
        print(f"✅ Success! {success_count} NEW schemes have been seeded into your database.")
        print("Go to your Citizen Portal to see the beautifully populated grid!")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    seed_database()