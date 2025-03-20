import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import zink as psst

def test01():
    text = "John works as a doctor and plays football after work and drives a toyota."
    labels = ("person","profession","sport","car")
    q = psst.redact(text, labels)
    assert "John" not in q.anonymized_text and "doctor" not in q.anonymized_text and "football" not in q.anonymized_text and "toyota" not in q.anonymized_text
    
def test02():
    text = "Samantha is sitting on a french chair"
    labels = ("person","furniture")
    q = psst.redact(text, labels)
    print(q.anonymized_text)
    assert "person_REDACTED" in q.anonymized_text and "furniture_REDACTED" in q.anonymized_text

def test03():
    text = "Patient, 33 years old, was admitted with a chest pain"
    labels = ("age","medical condition")
    q = psst.replace(text, labels)
    assert "33 years old" not in q.anonymized_text and "chest pain" not in q.anonymized_text

def test04():
    text = "John Doe dialled his mother at 992-234-3456 and then went out for a walk."
    labels = ("person","phone number","relationship")
    q = psst.replace(text, labels)
    assert "John Doe" not in q.anonymized_text and "992-234-3456" not in q.anonymized_text and "mother" not in q.anonymized_text

def test05():
    text = "Melissa is a software engineer at Google and she drives a Tesla. She is 29 years old. "
    labels = ("person","profession","company","car","age")
    my_data = {"person": "Jane", "profession": "Data Scientist", "company": "Amazon", "car": "Honda", "age": "35"}
    q = psst.replace_with_my_data(text,labels,my_data)
    assert "Melissa" not in q.anonymized_text and "software engineer" not in q.anonymized_text and "Google" not in q.anonymized_text and "Tesla" not in q.anonymized_text and "29 years old" not in q.anonymized_text