from data.database import (
    get_management_data,
    get_locality_data,
    get_occ_data,
    get_dafor_data
)

def test_all_queries():
    print("Testing all data queries...")
    
    tests = [
        ("Management Data", get_management_data),
        ("Locality Data", get_locality_data),
        ("Occurrence Data", get_occ_data),
        ("DAFOR Data", get_dafor_data)
    ]
    
    for name, query_func in tests:
        try:
            df = query_func()
            print(f"✓ {name} loaded successfully")
            print(f"Rows: {len(df)} | Columns: {list(df.columns)}")
            print("Sample data:")
            print(df.head(2))
            print("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"✗ Failed to load {name}: {str(e)}")

if __name__ == "__main__":
    test_all_queries()