import pandas as pd
from config.database import db
from sqlalchemy import text

class CoralDataService:
    def get_combined_data(self):
        """Combine data from your main tables"""
        localities = self._get_locality_data()
        occurrences = self._get_occurrence_data()
        
        # Simple merge - adjust based on your relationships
        df = pd.merge(
            occurrences,
            localities[['locality_id', 'name', 'coords_local']],
            on='locality_id',
            how='left'
        )
        
        # Convert coordinates if needed
        if 'coords_local' in df.columns:
            df[['latitude', 'longitude']] = df['coords_local'].apply(
                self._parse_coordinates
            )
        
        return df

    def _get_locality_data(self):
        """Get locality data from database"""
        with db.get_session() as session:
            result = session.execute(text("""
                SELECT locality_id, name, coords_local 
                FROM data_coralsol_locality
            """))
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def _get_occurrence_data(self):
        """Get occurrence data from database"""
        with db.get_session() as session:
            result = session.execute(text("""
                SELECT occurrence_id, locality_id, date, value 
                FROM data_coralsol_occurrence
            """))
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def _parse_coordinates(self, coord_string):
        """Simple coordinate parser - adjust for your format"""
        # Example: "(-8.052, -34.928)" → (-8.052, -34.928)
        if not coord_string:
            return (None, None)
        try:
            lat, lon = map(float, coord_string.strip("()").split(","))
            return (lat, lon)
        except:
            return (None, None)