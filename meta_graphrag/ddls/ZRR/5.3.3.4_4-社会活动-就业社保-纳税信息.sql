CREATE TABLE dwd_zrr_nsxx_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(200),
    nsrsbh CHAR(500),
    sz VARCHAR(400),
    zrrnsdxm VARCHAR(2400),
    sre NUMERIC,
    nssksssq CHAR(200),
    skssq INTEGER,
    ynssde NUMERIC,
    ynsl NUMERIC,
    jsje NUMERIC,
    sjse NUMERIC,
    jnsj DATE,
    zsjgmc VARCHAR(500),
    grsdssdnf CHAR(50),
    gszsjg CHAR(200),
    gsjnpzhm CHAR(300)
);

COMMENT ON TABLE dwd_zrr_nsxx_new IS '纳税信息';
COMMENT ON COLUMN dwd_zrr_nsxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_nsxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_nsxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_nsxx_new.nsrsbh IS '纳税人识别号';
COMMENT ON COLUMN dwd_zrr_nsxx_new.sz IS '税种';
COMMENT ON COLUMN dwd_zrr_nsxx_new.zrrnsdxm IS '自然人纳税所得项目';
COMMENT ON COLUMN dwd_zrr_nsxx_new.sre IS '收入额';
COMMENT ON COLUMN dwd_zrr_nsxx_new.nssksssq IS '纳税税款所属时期';
COMMENT ON COLUMN dwd_zrr_nsxx_new.skssq IS '税款所属期';
COMMENT ON COLUMN dwd_zrr_nsxx_new.ynssde IS '应纳税所得额';
COMMENT ON COLUMN dwd_zrr_nsxx_new.ynsl IS '应纳税率';
COMMENT ON COLUMN dwd_zrr_nsxx_new.jsje IS '缴税金额';
COMMENT ON COLUMN dwd_zrr_nsxx_new.sjse IS '实缴税额';
COMMENT ON COLUMN dwd_zrr_nsxx_new.jnsj IS '缴纳时间';
COMMENT ON COLUMN dwd_zrr_nsxx_new.zsjgmc IS '征税机构名称';
COMMENT ON COLUMN dwd_zrr_nsxx_new.grsdssdnf IS '个人所得税所得年份';
COMMENT ON COLUMN dwd_zrr_nsxx_new.gszsjg IS '个税征收机关';
COMMENT ON COLUMN dwd_zrr_nsxx_new.gsjnpzhm IS '个税缴纳凭证号码';