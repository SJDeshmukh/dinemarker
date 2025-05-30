import qrcode
import os

# Folder to save QR codes
output_folder = "employee_qrcodes"
os.makedirs(output_folder, exist_ok=True)

# Sample data for 10 Indian employees
employees = [
    {"name": "Aarav Sharma", "id": "EMP001", "section": "HR", "designation": "Manager"},
    {"name": "Saanvi Patel", "id": "EMP002", "section": "IT", "designation": "Software Engineer"},
    {"name": "Vihaan Mehta", "id": "EMP003", "section": "Finance", "designation": "Accountant"},
    {"name": "Diya Reddy", "id": "EMP004", "section": "Logistics", "designation": "Operations Lead"},
    {"name": "Aditya Nair", "id": "EMP005", "section": "Marketing", "designation": "Marketing Executive"},
    {"name": "Ishita Rao", "id": "EMP006", "section": "Sales", "designation": "Sales Associate"},
    {"name": "Karan Joshi", "id": "EMP007", "section": "Support", "designation": "Customer Support"},
    {"name": "Ananya Das", "id": "EMP008", "section": "Operations", "designation": "Process Analyst"},
    {"name": "Rohan Verma", "id": "EMP009", "section": "QA", "designation": "Quality Analyst"},
    {"name": "Meera Iyer", "id": "EMP010", "section": "Admin", "designation": "Admin Assistant"},
]

# Generate and save QR codes
for emp in employees:
    data = (
        f"Name: {emp['name']}\n"
        f"Employee ID: {emp['id']}\n"
        f"Section: {emp['section']}\n"
        f"Designation: {emp['designation']}"
    )
    qr = qrcode.make(data)
    filename = f"{emp['id']}_{emp['name'].replace(' ', '_')}.png"
    qr.save(os.path.join(output_folder, filename))

print(f"QR codes saved to '{output_folder}' folder.")
