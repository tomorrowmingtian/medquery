"""生成医疗数据库模拟数据 — 200患者，姓名和电话不重复，总数>200条"""
import random, datetime

random.seed(42)

def d(start, end):
    delta = (end - start).days
    return start + datetime.timedelta(days=random.randint(0, delta))

# ==================== 科室 (8) ====================
depts = [
    (1, '心血管内科', '住院部5楼', '020-85551201'),
    (2, '骨科',       '住院部7楼', '020-85551202'),
    (3, '儿科',       '门诊楼2楼', '020-85551203'),
    (4, '呼吸内科',   '住院部6楼', '020-85551204'),
    (5, '神经内科',   '住院部8楼', '020-85551205'),
    (6, '妇产科',     '住院部9楼', '020-85551206'),
    (7, '消化内科',   '住院部4楼', '020-85551207'),
    (8, '内分泌科',   '门诊楼3楼', '020-85551208'),
]

# ==================== 医生 (15) ====================
doctor_data = [
    (1, '张伟', '男', '主任医师', 1, '冠心病介入治疗'),
    (2, '李娜', '女', '副主任医师', 1, '心律失常与电生理'),
    (3, '王强', '男', '主任医师', 2, '脊柱外科与微创'),
    (4, '刘芳', '女', '主治医师', 3, '儿童呼吸与哮喘'),
    (5, '陈静', '女', '主任医师', 4, '慢性阻塞性肺病'),
    (6, '赵明', '男', '副主任医师', 5, '脑血管病与介入'),
    (7, '孙丽', '女', '主任医师', 6, '高危妊娠管理'),
    (8, '周涛', '男', '主治医师', 2, '关节镜与运动医学'),
    (9, '杨雪', '女', '副主任医师', 7, '炎症性肠病'),
    (10, '马超', '男', '主任医师', 8, '糖尿病与代谢病'),
    (11, '何敏', '女', '主治医师', 3, '新生儿疾病'),
    (12, '林峰', '男', '副主任医师', 5, '帕金森病与运动障碍'),
    (13, '黄玲', '女', '主治医师', 4, '支气管哮喘'),
    (14, '徐凯', '男', '主治医师', 7, '肝胆胰疾病'),
    (15, '宋婷', '女', '主任医师', 8, '甲状腺疾病'),
]

# ==================== 患者 (200) ====================
# 百家姓前80个
surnames = [
    '赵','钱','孙','李','周','吴','郑','王','冯','陈','褚','卫','蒋','沈','韩','杨',
    '朱','秦','尤','许','何','吕','施','张','孔','曹','严','华','金','魏','陶','姜',
    '戚','谢','邹','喻','柏','水','窦','章','云','苏','潘','葛','奚','范','彭','郎',
    '鲁','韦','昌','马','苗','凤','花','方','俞','任','袁','柳','酆','鲍','史','唐',
    '费','廉','岑','薛','雷','贺','倪','汤','滕','殷','罗','毕','郝','邬','安','常',
]

male_given = [
    '伟','强','军','勇','磊','涛','斌','杰','鹏','飞','建国','志强','文博','宇轩','浩然','明哲',
    '俊杰','子豪','一鸣','天乐','思远','力行','正则','知非','守仁','景行','修远','鸿飞','海东',
    '木森','怀瑾','北辰','书恒','逸凡','敬轩','若愚','承志','德厚','子昂','仲谦','伯安','叔同',
    '季康','云舟','星河','千帆','行之','卓然',
]

female_given = [
    '芳','娜','敏','静','丽','婷','雪','娟','秀兰','桂英','玉梅','晓红','慧敏','雅文','梦琪','雨桐',
    '思雨','若兰','知秋','婉清','晓月','如烟','念慈','灵犀','采薇','明瑾','佩兰','幼仪','望舒','清漪',
    '芯怡','乐瑶','钰涵','若曦','云舒','芷若','妙音','素心','映荷','含烟','碧落','秋词','雪见',
    '尔雅','文茵','蓁蓁','未央','星晚',
]

# 生成200个不重复姓名
used_names = set()
all_names = []
shuffled_s = surnames.copy()
random.shuffle(shuffled_s)
idx = 0
while len(all_names) < 200:
    s = shuffled_s[idx % len(shuffled_s)]
    idx += 1
    # 交替男女
    if random.random() < 0.5:
        g = random.choice(male_given)
    else:
        g = random.choice(female_given)
    full = s + g
    if full not in used_names:
        used_names.add(full)
        all_names.append(full)

# 生成200个不重复手机号
used_phones = set()
phones_list = []
while len(phones_list) < 200:
    ph = f"1{random.randint(30, 89):02d}{random.randint(10000000, 99999999)}"
    if ph not in used_phones:
        used_phones.add(ph)
        phones_list.append(ph)

streets = [
    '中山路','人民路','建设路','解放路','东风路','滨江路','天河路','环市路','江南大道',
    '黄埔大道','龙津路','景泰街','新华街','大学城外环','科学城主干道','体育西路',
    '广园路','新港路','同和路','大观路',
]
districts = ['天河区','越秀区','海珠区','番禺区','白云区','荔湾区','黄埔区','花都区','南沙区','增城区']

patients = []
date_base = datetime.date(2025, 1, 1)
date_end = datetime.date(2026, 1, 31)

fem_end_chars = {'芳','娜','敏','静','丽','婷','雪','娟','兰','英','梅','红','文','琪','桐',
                 '雨','萱','怡','瑶','钰','曦','云','心','婉','如','烟','念','灵','薇','明','瑾',
                 '佩','仪','舒','杏','思','秋','慧','雅','乐','蕾','露','清','月','芷','音','素',
                 '荷','碧','词','见','尔','茵','蓁','央','晚','若','涵','梦','漪','兮','瑶','妙'}

for i in range(200):
    name = all_names[i]
    gender = '女' if name[-1] in fem_end_chars else '男'
    age = random.randint(1, 92)
    phone = phones_list[i]
    addr = f"广州市{random.choice(districts)}{random.choice(streets)}{random.randint(1, 300)}号"
    adm = d(date_base, date_end)
    disch = d(adm, adm + datetime.timedelta(days=random.randint(2, 50))) if random.random() < 0.58 else None
    dept_id = random.randint(1, 8)
    patients.append((i+1, name, gender, age, phone, addr, adm.strftime('%Y-%m-%d'),
                     disch.strftime('%Y-%m-%d') if disch else None, dept_id))

# ==================== 诊断 ====================
disease_main = [
    ('2型糖尿病', '空腹血糖及糖化血红蛋白偏高，启动生活方式干预联合口服降糖药'),
    ('原发性高血压(2级)', '非同日三次测量血压均≥160/100mmHg'),
    ('冠状动脉粥样硬化性心脏病', '劳力性心绞痛表现，冠脉CTA确认'),
    ('急性心肌梗死(下壁)', '突发胸痛伴大汗，心电图II/III/avF导联ST段抬高'),
    ('腰椎间盘突出症(L4-L5)', '腰痛伴单侧下肢放射痛，直腿抬高试验阳性'),
    ('支气管肺炎', '发热咳嗽3天，双肺闻及湿啰音'),
    ('慢性阻塞性肺疾病(GOLD 2级)', '吸烟40年，肺功能提示FEV1/FVC<0.7'),
    ('急性脑梗死', '突发一侧肢体无力，头颅MRI DWI高信号'),
    ('社区获得性肺炎', '院外起病，发热咳嗽咳痰1周'),
    ('内侧半月板撕裂', '运动后关节绞索伴弹响，McMurray征阳性'),
    ('妊娠期糖尿病(A2级)', '孕28周OGTT两项异常，饮食控制欠佳'),
    ('胃溃疡(活动期)', '规律性上腹痛，胃镜见圆形溃疡'),
    ('甲状腺功能亢进症', '心悸手抖、体重减轻，TSH<0.01mIU/L'),
    ('肝硬化(代偿期)', '慢性乙肝病史，超声提示肝脏弥漫性病变'),
    ('急性胰腺炎(轻症)', '饮酒后上腹剧痛，血淀粉酶>500U/L'),
    ('慢性浅表性胃炎', '反复上腹不适，胃镜确诊'),
    ('阵发性心房颤动', '心悸伴脉搏短绌，Holter记录到房颤发作'),
    ('类风湿性关节炎', '对称性多关节肿痛，晨僵>1小时，CCP抗体阳性'),
    ('缺铁性贫血', '面色苍白伴乏力，血清铁蛋白<15ng/mL'),
    ('带状疱疹', '右侧胸背部簇集性水疱伴灼痛5天'),
    ('脑出血(基底节区)', '突发头痛呕吐，CT示基底节区高密度影'),
    ('前列腺增生', '进行性排尿困难，IPSS评分22分'),
    ('股骨颈骨折', '跌倒后右髋疼痛活动受限，X片确诊'),
    ('输尿管结石', '突发左侧腰腹绞痛伴血尿'),
    ('过敏性紫癜', '双下肢对称性紫癜伴腹痛'),
    ('肾病综合征', '大量蛋白尿(>3.5g/d)伴低白蛋白血症'),
    ('扩张型心肌病', '活动后气促，心脏扩大LVEF 32%'),
    ('重症肌无力', '眼睑下垂晨轻暮重，新斯的明试验阳性'),
    ('肝癌(原发性)', 'AFP>1000ng/mL，增强CT示肝内占位'),
    ('急性阑尾炎', '转移性右下腹痛，麦氏点压痛反跳痛'),
]

disease_sec = [
    '高脂血症', '高尿酸血症', '脂肪肝(轻度)', '低钾血症', '阻塞性睡眠呼吸暂停',
    '慢性肾功能不全(CKD3期)', '心力衰竭(NYHA II级)', '功能性便秘', '骨质疏松症',
    '广泛性焦虑障碍', '颈椎病(神经根型)', '下肢动脉粥样硬化', '胆囊息肉', '肾囊肿',
    '维生素D缺乏', '前列腺钙化', '肝囊肿', '糖耐量异常', '肥胖症(BMI 31)',
    '慢性咽炎', '白内障(初发期)', '胆囊结石', '反流性食管炎', '混合痔',
]

diagnoses = []
diag_id = 1
for p in patients:
    pid = p[0]
    adm = datetime.date.fromisoformat(p[6])
    main_disease, note = random.choice(disease_main)
    diag_date = d(adm, adm + datetime.timedelta(days=3))
    doc = random.choice([d[0] for d in doctor_data])
    diagnoses.append((diag_id, pid, doc, main_disease, '主要诊断', diag_date.strftime('%Y-%m-%d'), note))
    diag_id += 1

    if random.random() < 0.45:
        sec = random.choice(disease_sec)
        sec_date = d(diag_date, diag_date + datetime.timedelta(days=4))
        sec_doc = random.choice([d[0] for d in doctor_data])
        diagnoses.append((diag_id, pid, sec_doc, sec, '次要诊断', sec_date.strftime('%Y-%m-%d'), None))
        diag_id += 1

    if random.random() < 0.12:
        third = random.choice(disease_sec)
        third_date = d(diag_date, diag_date + datetime.timedelta(days=6))
        third_doc = random.choice([d[0] for d in doctor_data])
        diagnoses.append((diag_id, pid, third_doc, third, '次要诊断', third_date.strftime('%Y-%m-%d'), None))
        diag_id += 1

# ==================== 处方 ====================
drug_pool = [
    ('二甲双胍片', '500mg', '每日两次'),
    ('阿托伐他汀钙片', '20mg', '每晚一次'),
    ('苯磺酸氨氯地平片', '5mg', '每日一次'),
    ('阿司匹林肠溶片', '100mg', '每日一次'),
    ('硫酸氢氯吡格雷片', '75mg', '每日一次'),
    ('酒石酸美托洛尔片', '25mg', '每日两次'),
    ('布洛芬缓释胶囊', '300mg', '每日两次'),
    ('沙美特罗替卡松粉吸入剂', '50μg/250μg', '每日两次'),
    ('阿莫西林克拉维酸钾片', '375mg', '每日三次'),
    ('硝苯地平控释片', '30mg', '每日一次'),
    ('塞来昔布胶囊', '200mg', '每日一次'),
    ('门冬胰岛素注射液', '6IU', '每日三次(餐前)'),
    ('单硝酸异山梨酯缓释片', '40mg', '每日一次'),
    ('盐酸左氧氟沙星片', '500mg', '每日一次'),
    ('奥美拉唑肠溶胶囊', '20mg', '每日一次(晨服)'),
    ('华法林钠片', '2.5mg', '每日一次'),
    ('甘精胰岛素注射液', '10IU', '每晚睡前'),
    ('头孢呋辛酯片', '250mg', '每日两次'),
    ('蒙脱石散', '3g', '每日三次'),
    ('普瑞巴林胶囊', '75mg', '每日两次'),
    ('瑞舒伐他汀钙片', '10mg', '每晚一次'),
    ('厄贝沙坦片', '150mg', '每日一次'),
    ('碳酸钙D3咀嚼片', '600mg', '每日一次'),
    ('盐酸氨溴索口服液', '30mg', '每日三次'),
    ('呋塞米片', '20mg', '每日一次'),
    ('氯化钾缓释片', '1g', '每日两次'),
    ('甲钴胺片', '0.5mg', '每日三次'),
    ('阿卡波糖片', '50mg', '每日三次(餐时)'),
    ('泮托拉唑钠肠溶片', '40mg', '每日一次'),
    ('氯沙坦钾片', '50mg', '每日一次'),
    ('非布司他片', '40mg', '每日一次'),
    ('盐酸坦索罗辛缓释胶囊', '0.2mg', '每晚一次'),
    ('醋酸泼尼松片', '10mg', '每日一次'),
    ('格列美脲片', '2mg', '每日一次'),
    ('替格瑞洛片', '90mg', '每日两次'),
]

prescriptions = []
pres_id = 1
for p in patients:
    pid = p[0]
    adm = datetime.date.fromisoformat(p[6])
    disch_raw = p[7]
    disch = datetime.date.fromisoformat(disch_raw) if disch_raw is not None else None
    end_limit = disch if disch else adm + datetime.timedelta(days=60)

    n = random.choices([1, 2, 3, 4], weights=[0.25, 0.4, 0.25, 0.1])[0]
    for _ in range(n):
        drug = random.choice(drug_pool)
        start = d(adm, adm + datetime.timedelta(days=4))
        days_left = (end_limit - start).days
        if random.random() < 0.45 and days_left > 0:
            end = d(start, end_limit)
        else:
            end = None
        doc = random.choice([d[0] for d in doctor_data])
        cost = round(random.uniform(5.0, 500.0), 2)
        prescriptions.append((pres_id, pid, doc, drug[0], drug[1], drug[2],
                              start.strftime('%Y-%m-%d'),
                              end.strftime('%Y-%m-%d') if end else None, cost))
        pres_id += 1

# ==================== 检查 ====================
exam_pool = [
    ('检验', '血常规', 25.0, '白细胞{WBC}×10⁹/L，红细胞{RBC}×10¹²/L，血红蛋白{HGB}g/L，血小板{PLT}×10⁹/L'),
    ('检验', '空腹血糖', 35.0, '{GLU}mmol/L'),
    ('检验', '糖化血红蛋白(HbA1c)', 60.0, '{HBA1C}%'),
    ('检验', '血脂四项', 120.0, '总胆固醇{TCHO}mmol/L, 低密度脂蛋白{LDL}mmol/L, 高密度脂蛋白{HDL}mmol/L, 甘油三酯{TG}mmol/L'),
    ('检验', '肝功能全套', 180.0, 'ALT{ALT}U/L, AST{AST}U/L, 总胆红素{TBIL}μmol/L, 白蛋白{ALB}g/L'),
    ('检验', '肾功能电解质', 90.0, '肌酐{Cr}μmol/L, 尿素{BUN}mmol/L, 钾{K}mmol/L, 钠{Na}mmol/L'),
    ('检验', '高敏肌钙蛋白I', 150.0, '{TNI}ng/L(参考值<34)'),
    ('检验', '动脉血气分析', 120.0, 'pH{pH}, PaO2{PO2}mmHg, PaCO2{PCO2}mmHg, HCO3{HCO3}mmol/L'),
    ('检验', '尿常规+沉渣', 10.0, '蛋白{PRO}, 葡萄糖{GLU_u}, 潜血{BLD}, 白细胞{ULEU}'),
    ('检验', '凝血四项', 80.0, 'PT{PT}s, APTT{APTT}s, INR{INR}, FIB{FIB}g/L'),
    ('检验', '甲状腺功能五项', 150.0, 'TSH{TSH}mIU/L, FT3{FT3}pmol/L, FT4{FT4}pmol/L'),
    ('检验', '脑钠肽(BNP)', 200.0, '{BNP}pg/mL'),
    ('检验', '血淀粉酶', 40.0, '{AMY}U/L'),
    ('检验', '肿瘤标志物筛查', 350.0, 'AFP{AFP}ng/mL, CEA{CEA}ng/mL, CA19-9{CA199}U/mL'),
    ('检验', 'C反应蛋白', 30.0, '{CRP}mg/L'),
    ('影像', '胸部正位X片', 180.0, '双肺纹理{lung}，心影{heart_size}'),
    ('影像', '胸部CT平扫', 650.0, '肺野{lung_ct}，纵隔{mediastinum}，胸膜{pleura}'),
    ('影像', '头颅CT平扫', 450.0, '颅内{head}，中线结构{midline}'),
    ('影像', '头颅MRI+MRA', 1600.0, '脑实质{brain}，颅内血管{mra}'),
    ('影像', '冠脉CTA', 1800.0, '冠脉{coronary}，钙化积分{ca_score}'),
    ('影像', '腰椎MRI', 1200.0, '{spine}，椎旁软组织{paraspinal}'),
    ('影像', '膝关节MRI', 1200.0, '{knee}，交叉韧带{cruciate}'),
    ('影像', '腹部彩超', 200.0, '肝脏{liver}，胆囊{gallbladder}，胰腺{pancreas}，脾脏{spleen}'),
    ('影像', '心脏彩色多普勒', 480.0, 'LVEF{ef}%，室壁运动{wall}，瓣膜{valve}'),
    ('影像', '颈部血管超声', 300.0, '双侧颈总动脉{carotid}，IMT{imt}mm'),
    ('心电', '24h动态心电图', 280.0, '{holter}，平均心率{avg_hr}次/分'),
    ('心电', '常规12导联心电图', 50.0, '窦性心律，{ecg}'),
    ('内镜', '胃镜检查', 380.0, '食道{esophagus}，胃黏膜{gastric}，十二指肠{duodenum}'),
    ('内镜', '结肠镜检查', 520.0, '回盲部{ileocecal}，结肠{colon}，直肠{rectum}'),
]

def gen_result(tpl):
    s = {
        'WBC': round(random.uniform(2.8, 19.0), 1),
        'RBC': round(random.uniform(2.5, 6.5), 1),
        'HGB': int(round(random.uniform(68, 180), 0)),
        'PLT': int(round(random.uniform(80, 450), 0)),
        'GLU': round(random.uniform(3.5, 18.0), 1),
        'HBA1C': round(random.uniform(4.8, 11.5), 1),
        'TCHO': round(random.uniform(3.0, 8.5), 1),
        'LDL': round(random.uniform(1.2, 6.0), 1),
        'HDL': round(random.uniform(0.5, 2.5), 1),
        'TG': round(random.uniform(0.4, 6.0), 1),
        'ALT': random.randint(8, 250), 'AST': random.randint(8, 220),
        'TBIL': round(random.uniform(3.5, 50.0), 1),
        'ALB': round(random.uniform(28.0, 50.0), 1),
        'Cr': round(random.uniform(40, 350), 0), 'BUN': round(random.uniform(2.5, 18.0), 1),
        'K': round(random.uniform(2.8, 5.8), 1), 'Na': round(random.uniform(130, 150), 0),
        'TNI': round(random.uniform(1, 2500), 0),
        'pH': round(random.uniform(7.20, 7.50), 2),
        'PO2': round(random.uniform(45, 100), 0), 'PCO2': round(random.uniform(25, 60), 0),
        'HCO3': round(random.uniform(16, 32), 1),
        'PRO': random.choice(['阴性','±','+','++','+++']),
        'GLU_u': random.choice(['阴性','+','++']),
        'BLD': random.choice(['阴性','+','++']),
        'ULEU': random.choice(['阴性','±','+']),
        'PT': round(random.uniform(9.0, 20.0), 1), 'APTT': round(random.uniform(22.0, 50.0), 1),
        'INR': round(random.uniform(0.80, 2.50), 2), 'FIB': round(random.uniform(1.5, 5.5), 1),
        'TSH': round(random.uniform(0.005, 18.0), 3), 'FT3': round(random.uniform(2.0, 14.0), 1),
        'FT4': round(random.uniform(6.0, 38.0), 1),
        'BNP': random.randint(20, 3500),
        'AMY': random.randint(30, 850),
        'AFP': round(random.uniform(1.5, 800.0), 1),
        'CEA': round(random.uniform(1.0, 45.0), 1),
        'CA199': round(random.uniform(5.0, 200.0), 1),
        'CRP': round(random.uniform(1.0, 120.0), 1),
        'lung': random.choice(['未见异常','纹理增多增粗','片状渗出影','索条状高密度影']),
        'heart_size': random.choice(['未见增大','心影增大','肺动脉段突出']),
        'lung_ct': random.choice(['未见异常密度','肺气肿改变','磨玻璃密度影','多发实性微小结节']),
        'mediastinum': random.choice(['未见肿大淋巴结','纵隔淋巴结稍大','纵隔居中']),
        'pleura': random.choice(['光滑','胸膜增厚','少量胸腔积液']),
        'head': random.choice(['颅内未见异常','基底节区腔隙性低密度灶','多发腔梗']),
        'midline': random.choice(['居中','居中未见移位']),
        'brain': random.choice(['脑实质未见异常信号','脑白质疏松(Fazekas 1级)','左侧基底节区陈旧性腔梗','老年性脑改变','多发缺血性白质病变']),
        'mra': random.choice(['未见明显狭窄','左侧大脑中动脉M1段轻度狭窄','颈内动脉起始部斑块']),
        'coronary': random.choice(['未见明显狭窄','左前降支近段30%狭窄','右冠状动脉中段50%狭窄','前降支多发混合斑块伴管腔轻中度狭窄']),
        'ca_score': random.randint(0, 420),
        'spine': random.choice(['L4-5椎间盘膨出','L5-S1椎间盘向左后方突出','腰椎退行性变','L3-S1椎间盘不同程度突出']),
        'paraspinal': random.choice(['未见异常','腰大肌旁未见异常']),
        'knee': random.choice(['关节腔少量积液','内侧半月板后角III级损伤信号','前交叉韧带增粗信号增高','髌骨软骨软化']),
        'cruciate': random.choice(['未见异常','前交叉韧带连续','后交叉韧带形态信号可']),
        'liver': random.choice(['形态未见异常','轻度脂肪浸润','回声增粗','肝囊肿']),
        'gallbladder': random.choice(['壁光滑','壁毛糙增厚','多发结石','息肉样病变']),
        'pancreas': random.choice(['未见异常','胰头饱满']), 'spleen': random.choice(['未见异常','轻度肿大']),
        'ef': random.randint(30, 72),
        'wall': random.choice(['未见节段性运动异常','左室壁运动弥漫性减低','室间隔基底段增厚']),
        'valve': random.choice(['未见反流','二尖瓣少量反流','主动脉瓣钙化伴轻度狭窄']),
        'carotid': random.choice(['内膜光滑','内膜增厚伴斑块形成','混合性斑块致管腔轻度狭窄']),
        'imt': round(random.uniform(0.6, 1.8), 1),
        'holter': random.choice(['偶发房性早搏','频发室性早搏','阵发性心房颤动','ST-T动态改变','未见明显异常']),
        'avg_hr': random.randint(52, 105),
        'ecg': random.choice(['正常心电图','T波低平','ST段轻度下移','左室高电压','不完全右束支传导阻滞']),
        'esophagus': random.choice(['光滑通畅','下段黏膜充血']),
        'gastric': random.choice(['未见异常','胃窦黏膜花斑样充血','胃角见浅溃疡','胃体大弯侧糜烂']),
        'duodenum': random.choice(['球部未见异常','球部霜斑样溃疡','降段黏膜光滑']),
        'ileocecal': random.choice(['未见异常','回盲瓣形态正常']),
        'colon': random.choice(['未见异常','乙状结肠见0.6cm息肉','升结肠见憩室','横结肠黏膜充血水肿']),
        'rectum': random.choice(['黏膜光滑','内痔','混合痔']),
    }
    return tpl.format(**s)

examinations = []
exam_id = 1
for p in patients:
    pid = p[0]
    adm = datetime.date.fromisoformat(p[6])
    n = random.choices([1, 2, 3, 4], weights=[0.2, 0.4, 0.3, 0.1])[0]
    for _ in range(n):
        etype, eitem, ecost, etpl = random.choice(exam_pool)
        edate = d(adm, adm + datetime.timedelta(days=8))
        doc = random.choice([d[0] for d in doctor_data])
        result = gen_result(etpl)
        examinations.append((exam_id, pid, doc, etype, eitem, edate.strftime('%Y-%m-%d'), result, ecost))
        exam_id += 1

# ==================== 生理指标 ====================
metrics = []
met_id = 1
for p in patients:
    pid = p[0]
    adm = datetime.date.fromisoformat(p[6])
    disch_raw = p[7]
    disch = datetime.date.fromisoformat(disch_raw) if disch_raw is not None else None
    end = disch if disch else adm + datetime.timedelta(days=14)
    stay = (end - adm).days if end else 14

    measures = [adm]
    if stay > 1:
        n_extra = min(random.randint(1, 10), stay - 1)
        for ed in sorted(random.sample(range(1, stay), n_extra)):
            measures.append(adm + datetime.timedelta(days=ed))
    if disch and disch != adm:
        measures.append(disch)

    base_hr = random.randint(58, 110)
    base_sys = random.randint(95, 182)
    base_dia = random.randint(55, 110)
    base_temp = round(random.uniform(36.1, 39.0), 1)
    base_bs = round(random.uniform(3.8, 13.0), 2)
    base_spo2 = round(random.uniform(88.0, 99.0), 1)
    base_rr = random.randint(13, 28)

    for mday in measures:
        hr = max(40, min(150, base_hr + random.randint(-12, 12)))
        sys = max(80, min(210, base_sys + random.randint(-18, 18)))
        dia = max(45, min(128, base_dia + random.randint(-12, 12)))
        temp = round(max(35.5, min(41.5, base_temp + random.uniform(-0.7, 0.6))), 1)
        bs = round(max(2.2, min(24.0, base_bs + random.uniform(-2.0, 1.5))), 2)
        spo2 = round(max(82.0, min(100.0, base_spo2 + random.uniform(-3.0, 2.5))), 1)
        rr = max(8, min(38, base_rr + random.randint(-5, 5)))

        note = None
        if mday == measures[0]:
            note = '入院首次测量'
        elif disch and mday == disch:
            note = '出院前测量'

        md = f"{mday.strftime('%Y-%m-%d')} {random.randint(6, 10):02d}:{random.choice([0, 15, 30, 45]):02d}:00"
        metrics.append((met_id, pid, md, hr, sys, dia, temp, bs, spo2, rr, note))
        met_id += 1

# ==================== 输出 ====================
def to_val(v):
    if v is None: return 'NULL'
    if isinstance(v, int): return str(v)
    if isinstance(v, float): return str(v)
    s = str(v).replace("'", "''").replace("\\", "\\\\")
    return f"'{s}'"

def gen_insert(table, cols, rows):
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n"
    sql += ",\n".join("(" + ", ".join(to_val(c) for c in r) + ")" for r in rows) + ";\n"
    return sql

total = len(depts)+len(doctor_data)+len(patients)+len(diagnoses)+len(prescriptions)+len(examinations)+len(metrics)

sql = f"""-- ============================================================
-- 医疗数据库模拟数据
-- 科室: {len(depts)} | 医生: {len(doctor_data)} | 患者: {len(patients)}
-- 诊断: {len(diagnoses)} | 处方: {len(prescriptions)} | 检查: {len(examinations)} | 生理指标: {len(metrics)}
-- 总计: {total} 条
-- ============================================================

"""

sql += gen_insert('departments', ['id','name','location','phone'], depts)
sql += "\n"
sql += gen_insert('doctors', ['id','name','gender','title','department_id','specialty'], doctor_data)
sql += "\n"
sql += gen_insert('patients', ['id','name','gender','age','phone','address','admission_date','discharge_date','department_id'], patients)
sql += "\n"
sql += gen_insert('diagnoses', ['id','patient_id','doctor_id','disease_name','diagnosis_type','diagnosis_date','notes'], diagnoses)
sql += "\n"
sql += gen_insert('prescriptions', ['id','patient_id','doctor_id','drug_name','dosage','frequency','start_date','end_date','cost'], prescriptions)
sql += "\n"
sql += gen_insert('examinations', ['id','patient_id','doctor_id','exam_type','exam_item','exam_date','result','cost'], examinations)
sql += "\n"
sql += gen_insert('metrics', ['id','patient_id','measure_date','heart_rate','systolic_pressure','diastolic_pressure',
    'temperature','blood_sugar','oxygen_saturation','respiratory_rate','notes'], metrics)
sql += "\n"

for tbl, n in [('departments',len(depts)),('doctors',len(doctor_data)),('patients',len(patients)),
               ('diagnoses',len(diagnoses)),('prescriptions',len(prescriptions)),
               ('examinations',len(examinations)),('metrics',len(metrics))]:
    sql += f"ALTER TABLE {tbl} AUTO_INCREMENT = {n+1};\n"

with open('D:/medquery/sql/mock_data.sql', 'w', encoding='utf-8') as f:
    f.write(sql)

print(f"科室: {len(depts)}")
print(f"医生: {len(doctor_data)}")
print(f"患者: {len(patients)}")
print(f"诊断: {len(diagnoses)}")
print(f"处方: {len(prescriptions)}")
print(f"检查: {len(examinations)}")
print(f"生理指标: {len(metrics)}")
print(f"总计: {total} 条")
print("Done → sql/mock_data.sql")
