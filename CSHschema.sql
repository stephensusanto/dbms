DROP TABLE IF EXISTS Administrator;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS AdmissionType;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Admission;

CREATE TABLE Administrator (
    UserName VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(20) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(20) NOT NULL
);

INSERT INTO Administrator VALUES 
('jdoe', 'Pass1234', 'John', 'Doe', 'jdoe@csh.com'),
('jsmith', 'Pass5678', 'Jane', 'Smith', 'jsmith@csh.com'),
('ajohnson', 'Passabcd', 'Alice', 'Johnson', 'ajohnson@csh.com'),
('bbrown', 'Passwxyz', 'Bob', 'Brown', 'bbrown@csh.com'),
('cdavis', 'Pass9876', 'Charlie', 'Davis', 'cdavis@csh.com'),
('ksmith', 'Pass5566', 'Karen', 'Smith', 'ksmith@csh.com');

CREATE TABLE Patient (
    PatientID VARCHAR(10) PRIMARY KEY,
    Password VARCHAR(20) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Mobile VARCHAR(20) NOT NULL
);

INSERT INTO Patient VALUES 
('dwilson', 'Pass5432', 'David', 'Wilson', '4455667788'),
('etylor', 'Passlmno', 'Eva', 'Taylor', '5566778899'),
('faderson', 'Passrstu', 'Frank', 'Anderson', '6677889900'),
('gthomas', 'Pass1357', 'Grace', 'Thomas', '7788990011'),
('smartinez', 'Pass2468', 'Stan', 'Martinez', '8899001122'),
('lroberts', 'Pass1122', 'Laura', 'Roberts', '9900112233');


CREATE TABLE AdmissionType (
    AdmissionTypeID SERIAL PRIMARY KEY,
    AdmissionTypeName VARCHAR(20) UNIQUE NOT NULL
);

INSERT INTO AdmissionType VALUES (1, 'Emergency');
INSERT INTO AdmissionType VALUES (2, 'Transfer');
INSERT INTO AdmissionType VALUES (3, 'Inpatient');
INSERT INTO AdmissionType VALUES (4, 'Outpatient');

CREATE TABLE Department (
    DeptId SERIAL PRIMARY Key,
    DeptName VARCHAR(20) UNIQUE not NULL
);

INSERT INTO Department VALUES (1, 'General');
INSERT INTO Department VALUES (2, 'Emergency');
INSERT INTO Department VALUES (3, 'Surgery');
INSERT INTO Department VALUES (4, 'Obstetrics');
INSERT INTO Department VALUES (5, 'Rehabilitation');
INSERT INTO Department VALUES (6, 'Paediatrics');

CREATE table Admission (
    AdmissionID SERIAL PRIMARY KEY,
    AdmissionType INTEGER NOT NULL,
    Department INTEGER NOT NULL,
	Patient VARCHAR(10) NOT NULL,
	Administrator VARCHAR(10) NOT NULL,
    Fee Decimal(7,2),
    DischargeDate Date,
    Condition VARCHAR(500),
	FOREIGN KEY(AdmissionType) REFERENCES AdmissionType,
	FOREIGN KEY(Department) REFERENCES Department,
	FOREIGN KEY(Patient) REFERENCES Patient,
	FOREIGN KEY(Administrator) REFERENCES Administrator
);

-- SET datestyle to DMY because of environment setting issues
SET datestyle TO 'DMY';

INSERT INTO Admission (AdmissionType, Department, Fee, Patient, Administrator, DischargeDate, Condition) VALUES
    (4, 1, 666.00, 'lroberts', 'jdoe', '28/02/2024', 'a red patch on my skin that looks irritated. It started small but has been spreading and feels warm to the touch'),
	(2, 1, 100.00, 'gthomas', 'jdoe', '11/09/2021', NULL),
	(1, 2, NULL, 'lroberts','jsmith', '02/09/2019', 'Admitted to the emergency department after suffering head trauma from a fall, requiring a CT scan and observation for potential concussion.'),
	(2, 3, 7688.00, 'dwilson','ajohnson', '01/12/2022', NULL),
	(2, 6, 1600.00, 'faderson', 'ajohnson', '03/09/2014', 'Child admitted to the hospital with a severe asthma attack, requiring oxygen therapy and nebulizer treatment.'),
	(4, 1, 90.00, 'gthomas', 'ksmith', '04/07/2021', 'Routine follow-up consultation to review progress after recent knee surgery, with positive recovery observed.'),
	(1, 2, 1450.00, 'smartinez', 'jsmith', NULL, 'Admitted to the emergency department with severe food poisoning, requiring IV fluids and anti-nausea medication for recovery.'),
	(4, 5, 180.95, 'dwilson', 'cdavis', '06/11/2021', 'Attended a physiotherapy session as part of an ongoing rehabilitation program following shoulder surgery.'),
	(3, 1, 2000.00, 'etylor', 'ajohnson', '10/09/2021', NULL),
	(2, 4, 8290.00, 'gthomas', 'jsmith', '01/09/2024', 'Postpartum care following a natural childbirth, including monitoring of both the mother and the newborn for potential complications.'),
	(2, 6, 1800.00, 'faderson', 'bbrown',  NULL, 'Child admitted to the paediatrics department for severe pneumonia, requiring intravenous antibiotics and respiratory therapy.'),
	(4, 1, 75.00, 'gthomas', 'bbrown', '19/11/2023', 'Routine general practitioner consultation for a follow-up after a recent bout of seasonal allergies.'),
	(3, 3, 7000.50, 'smartinez', 'jdoe', '15/10/2024', NULL),
	(1, 2, NULL, 'etylor', 'jdoe', NULL, 'I am having intense, crushing pain in my chest that feels like an elephant is sitting on it. It is spreading to my left arm and neck.');


--------------------------------------------- STORE PROCEDURE------------------------------------------------------

-----------------------------#####################Login Process#####################-----------------------------

CREATE OR REPLACE FUNCTION login_process(login VARCHAR, pass VARCHAR) RETURNS
TABLE(username VARCHAR(10), FirstName VARCHAR(50), LastName VARCHAR(50), Email VARCHAR(20)) AS $$
	BEGIN
		RETURN QUERY
			SELECT a.username, a.firstname, a.lastname, a.email
			FROM administrator AS a
			-- Username case insensitive
			WHERE LOWER(a.username) = LOWER(login) AND password = pass;
	END; 
$$ LANGUAGE plpgsql;

-----------------------------#####################Admission based on login#####################-----------------------------

CREATE OR REPLACE FUNCTION admission_data_based_on_login(login VARCHAR) RETURNS
TABLE(admission_id INTEGER,
		admission_type VARCHAR(50), 
		admission_department VARCHAR(50), 
		discharge_date VARCHAR(10), 
		fee DECIMAL(7,2), 
		patient VARCHAR(100), 
		condition VARCHAR(500)) AS $$
		BEGIN
			RETURN QUERY
				SELECT a.admissionid as admission_id, 
				admissiontype.admissiontypename as admission_type, 
				department.deptname as admission_department, 
				COALESCE(TO_CHAR(a.dischargedate, 'DD-MM-YYYY'), '')::VARCHAR as discharge_date, 
				COALESCE(a.fee, 0), 
				CONCAT(patient.firstname,' ',patient.lastname)::VARCHAR as patient, 
				COALESCE(a.condition, '') as condition
				FROM admission as a 
				INNER JOIN admissiontype ON admissiontype.admissiontypeid = a.admissiontype
				INNER JOIN department ON department.deptid = a.department
				INNER JOIN patient ON patient.patientid = a.patient
				WHERE administrator = login
				ORDER BY
				    a.dischargedate DESC NULLS LAST,
				    patient.firstname ASC,
				    admissiontype.admissiontypename DESC;
		END;
$$ LANGUAGE plpgsql

-----------------------------#####################Adding New Admission#####################-----------------------------
--DROP FUNCTION add_admission;
CREATE OR REPLACE FUNCTION add_admission(
    admission_type VARCHAR,
  	dept VARCHAR,
    patient_id VARCHAR,
    admin_name VARCHAR,
    patient_condition VARCHAR
)
RETURNS void
AS $$
BEGIN
    INSERT INTO admission(AdmissionType, Department, Patient, Administrator, Condition)
    VALUES((SELECT admissiontype.AdmissionTypeID from admissiontype WHERE admissiontype.AdmissionTypeName = admission_type), 
	(SELECT department.DeptId from department WHERE DeptName = dept), 
	patient_id, 
	admin_name, 
	patient_condition);
END;
$$
LANGUAGE plpgsql;

-----------------------------#####################Updating an Admission#####################-----------------------------
--DROP FUNCTION update_admission;
CREATE OR REPLACE FUNCTION update_admission(
	admission_id INTEGER,
    admission_type VARCHAR,
  	dept VARCHAR,
    update_dischargeDate Date,
	update_fee Decimal(7,2),
    patient_id VARCHAR,
    patient_condition VARCHAR
)
RETURNS void
AS $$
BEGIN
    UPDATE admission
    SET 
		AdmissionType = (SELECT admissiontype.AdmissionTypeID from admissiontype WHERE admissiontype.AdmissionTypeName = admission_type), 
		Department = (SELECT department.DeptId from department WHERE DeptName = dept),
		DischargeDate = update_dischargeDate,
		Fee = update_fee,
		Patient = patient_id,  
		Condition = patient_condition
	WHERE AdmissionID = admission_id;
END;
$$
LANGUAGE plpgsql;