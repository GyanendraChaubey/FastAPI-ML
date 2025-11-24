from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("patient.json", "r") as f:
        data = f.read()
    return json.loads(data)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def About():
    return {"message": "A Fully functional Patient Management System API"}

@app.get("/view")
def view_patients():
    patients = load_data()
    return patients


@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., title="The ID of the patient to retrieve", example="PAT001")):
    patients = load_data()
    patient = patients.get(patient_id)
    if patient:
        return patient
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(sort_by: str = Query(..., title="Sort on the basis of age"), order: str = Query("asc", description="Order of sorting: asc or desc")):
    valid_fields = ["age"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Can only sort by age")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")
    
    patients = load_data()
    
    sorted_patients = sorted(patients.values(), key=lambda x: x["age"], reverse=(order == "desc"))
    return sorted_patients
    

