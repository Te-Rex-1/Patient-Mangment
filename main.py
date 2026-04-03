from fastapi.responses import JSONResponse
from fastapi import FastAPI,Path,HTTPException,Query
from baseClass import Patient,Patient_Update
import json


app=FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/view')
def view():
    data=load_data()
    return  data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', examples='P001')):
    # load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'),
                  order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient:Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exist")
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})


@app.put('/update/{patient_id}')
def update_patient(patient_id:str,patient_update:Patient_Update):

    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')

    existing_patient_info=data[patient_id]
    updated_patient=patient_update.model_dump(exclude_unset=True)

    existing_patient_info.update(updated_patient)

    validate_patient=Patient(id=patient_id,**existing_patient_info)
    # conv  obj->:dict


    data[patient_id]=validate_patient.model_dump(exclude=['id'])

    save_data(data)
    return JSONResponse(status_code=200, content={'message':'patient updated'})



@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient deleted'})
