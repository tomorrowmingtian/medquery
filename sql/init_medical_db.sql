-- ============================================================
-- 医疗数据库初始化脚本
-- 数据库: medical_db  (7表)
-- ============================================================

CREATE DATABASE IF NOT EXISTS medical_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE medical_db;

-- 删除已有表（按外键依赖逆序）
DROP TABLE IF EXISTS metrics;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS examinations;
DROP TABLE IF EXISTS diagnoses;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS departments;

-- ------------------------------
-- 1. 科室信息表
-- ------------------------------
CREATE TABLE departments (
    id       INT PRIMARY KEY AUTO_INCREMENT,
    name     VARCHAR(50)  NOT NULL COMMENT '科室名称',
    location VARCHAR(50)  COMMENT '所在楼层',
    phone    VARCHAR(20)  COMMENT '联系电话'
) COMMENT '科室信息表';

-- ------------------------------
-- 2. 医生信息表
-- ------------------------------
CREATE TABLE doctors (
    id            INT PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(50)  NOT NULL COMMENT '医生姓名',
    gender        VARCHAR(5)   COMMENT '性别',
    title         VARCHAR(30)  COMMENT '职称',
    department_id INT          NOT NULL COMMENT '所属科室',
    specialty     VARCHAR(100) COMMENT '专业方向',
    FOREIGN KEY (department_id) REFERENCES departments(id)
) COMMENT '医生信息表';

-- ------------------------------
-- 3. 患者信息表
-- ------------------------------
CREATE TABLE patients (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(50)  NOT NULL COMMENT '患者姓名',
    gender          VARCHAR(5)   COMMENT '性别',
    age             INT          COMMENT '年龄',
    phone           VARCHAR(20)  COMMENT '联系电话',
    address         VARCHAR(200) COMMENT '住址',
    admission_date  DATE         COMMENT '入院日期',
    discharge_date  DATE         COMMENT '出院日期',
    department_id   INT          COMMENT '所属科室',
    FOREIGN KEY (department_id) REFERENCES departments(id)
) COMMENT '患者信息表';

-- ------------------------------
-- 4. 诊断记录表
-- ------------------------------
CREATE TABLE diagnoses (
    id             INT PRIMARY KEY AUTO_INCREMENT,
    patient_id     INT          NOT NULL COMMENT '患者ID',
    doctor_id      INT          COMMENT '主治医生ID',
    disease_name   VARCHAR(100) NOT NULL COMMENT '疾病名称',
    diagnosis_type VARCHAR(20)  DEFAULT '主要诊断' COMMENT '诊断类型',
    diagnosis_date DATE         COMMENT '诊断日期',
    notes          TEXT         COMMENT '备注',
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id)  REFERENCES doctors(id)
) COMMENT '诊断记录表';

-- ------------------------------
-- 5. 处方记录表
-- ------------------------------
CREATE TABLE prescriptions (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT           NOT NULL COMMENT '患者ID',
    doctor_id  INT           COMMENT '开方医生ID',
    drug_name  VARCHAR(100)  NOT NULL COMMENT '药品名称',
    dosage     VARCHAR(50)   COMMENT '剂量',
    frequency  VARCHAR(50)   COMMENT '用药频次',
    start_date DATE          COMMENT '开始日期',
    end_date   DATE          COMMENT '结束日期',
    cost       DECIMAL(10,2) COMMENT '费用(元)',
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id)  REFERENCES doctors(id)
) COMMENT '处方记录表';

-- ------------------------------
-- 6. 检查记录表
-- ------------------------------
CREATE TABLE examinations (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT           NOT NULL COMMENT '患者ID',
    doctor_id  INT           COMMENT '开单医生ID',
    exam_type  VARCHAR(50)   COMMENT '检查类型(影像/检验/心电等)',
    exam_item  VARCHAR(100)  COMMENT '检查项目名称',
    exam_date  DATE          COMMENT '检查日期',
    result     TEXT          COMMENT '检查结果',
    cost       DECIMAL(10,2) COMMENT '费用(元)',
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id)  REFERENCES doctors(id)
) COMMENT '检查记录表';

-- ------------------------------
-- 7. 生理指标记录表
-- ------------------------------
CREATE TABLE metrics (
    id                INT PRIMARY KEY AUTO_INCREMENT,
    patient_id        INT          NOT NULL COMMENT '患者ID',
    measure_date      DATETIME     COMMENT '测量时间',
    heart_rate        INT          COMMENT '心率(次/分)',
    systolic_pressure INT          COMMENT '收缩压(mmHg)',
    diastolic_pressure INT         COMMENT '舒张压(mmHg)',
    temperature       DECIMAL(3,1) COMMENT '体温(℃)',
    blood_sugar       DECIMAL(5,2) COMMENT '血糖(mmol/L)',
    oxygen_saturation DECIMAL(4,1) COMMENT '血氧饱和度(%)',
    respiratory_rate  INT          COMMENT '呼吸频率(次/分)',
    notes             VARCHAR(200) COMMENT '备注',
    FOREIGN KEY (patient_id) REFERENCES patients(id)
) COMMENT '生理指标记录表';
