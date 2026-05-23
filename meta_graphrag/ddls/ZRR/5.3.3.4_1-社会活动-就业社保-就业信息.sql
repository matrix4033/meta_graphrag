CREATE TABLE dwd_zrr_jyxx_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    cyzk VARCHAR(800),
    cjgzsj DATE,
    csdqzyqsnf CHAR(4),
    zylb CHAR(255),
    zymc CHAR(255),
    jrdpsj VARCHAR(50),
    gzdwmc VARCHAR(800),
    gzdwztlx VARCHAR(800),
    gzdwtyshxydm CHAR(18),
    szgzdwbmmc VARCHAR(200),
    gzdwtxdz VARCHAR(800),
    gzdwcz VARCHAR(50),
    gzdwdhhm VARCHAR(50),
    ldhtqsrq VARCHAR(50),
    ldhtzzrq DATE,
    rzrq VARCHAR(800),
    lzrq VARCHAR(800),
    gwlb VARCHAR(32),
    xrgwsj VARCHAR(300)
);

COMMENT ON TABLE dwd_zrr_jyxx_new IS '就业信息';
COMMENT ON COLUMN dwd_zrr_jyxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_jyxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_jyxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_jyxx_new.cyzk IS '从业状况';
COMMENT ON COLUMN dwd_zrr_jyxx_new.cjgzsj IS '参加工作时间';
COMMENT ON COLUMN dwd_zrr_jyxx_new.csdqzyqsnf IS '从事当前专业起始年份';
COMMENT ON COLUMN dwd_zrr_jyxx_new.zylb IS '职业类别';
COMMENT ON COLUMN dwd_zrr_jyxx_new.zymc IS '职业名称';
COMMENT ON COLUMN dwd_zrr_jyxx_new.jrdpsj IS '加入党派时间';
COMMENT ON COLUMN dwd_zrr_jyxx_new.gzdwmc IS '工作单位名称';
COMMENT ON COLUMN dwd_zrr_jyxx_new.gzdwztlx IS '工作单位主体类型';
COMMENT ON COLUMN dwd_zrr_jyxx_new.gzdwtyshxydm IS '工作单位统一社会信用代码';
COMMENT ON COLUMN dwd_zrr_jyxx_new.szgzdwbmmc IS '工作单位部门名称';
COMMENT ON COLUMN dwd_zrr_jyxx_new.gzdwtxdz IS '工作单位通信地址';
COMMENT ON COLUMN dwd_zrr_jyxx_new.gzdwcz IS '工作单位传真';
COMMENT ON COLUMN dwd_zrr_jyxx_new.gzdwdhhm IS '工作单位电话号码';
COMMENT ON COLUMN dwd_zrr_jyxx_new.ldhtqsrq IS '劳动合同起始日期';
COMMENT ON COLUMN dwd_zrr_jyxx_new.ldhtzzrq IS '劳动合同终止日期';
COMMENT ON COLUMN dwd_zrr_jyxx_new.rzrq IS '入职日期';
COMMENT ON COLUMN dwd_zrr_jyxx_new.lzrq IS '离职日期';
COMMENT ON COLUMN dwd_zrr_jyxx_new.gwlb IS '岗位类别';
COMMENT ON COLUMN dwd_zrr_jyxx_new.xrgwsj IS '现任岗位时间';