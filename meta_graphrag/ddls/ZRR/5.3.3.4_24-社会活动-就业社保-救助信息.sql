CREATE TABLE dwd_zrr_jzxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    shjzlb VARCHAR(80),
    jzzbh VARCHAR(400),
    jzksrq DATE,
    jzlb VARCHAR(1024),
    jzfs VARCHAR(256),
    jzyy VARCHAR(32000),
    sfbdhj VARCHAR(128),
    cjlb CHAR(128),
    cjdj VARCHAR(160),
    jtbh VARCHAR(1600),
    tdjzdxlbmc VARCHAR(800),
    dblx VARCHAR(1024),
    dbjtlqje NUMERIC,
    dbjzyxzh VARCHAR(1600),
    dbjzyxmc VARCHAR(400),
    jtzsr NUMERIC,
    zpyy CHAR(16)
);

COMMENT ON TABLE dwd_zrr_jzxx_new IS '救助信息';
COMMENT ON COLUMN dwd_zrr_jzxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_jzxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_jzxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_jzxx_new.shjzlb IS '社会救助类别';
COMMENT ON COLUMN dwd_zrr_jzxx_new.jzzbh IS '救助证编号';
COMMENT ON COLUMN dwd_zrr_jzxx_new.jzksrq IS '救助开始日期';
COMMENT ON COLUMN dwd_zrr_jzxx_new.jzlb IS '救助类别';
COMMENT ON COLUMN dwd_zrr_jzxx_new.jzfs IS '救助方式';
COMMENT ON COLUMN dwd_zrr_jzxx_new.jzyy IS '救助原因';
COMMENT ON COLUMN dwd_zrr_jzxx_new.sfbdhj IS '是否本地户籍';
COMMENT ON COLUMN dwd_zrr_jzxx_new.cjlb IS '残疾类别';
COMMENT ON COLUMN dwd_zrr_jzxx_new.cjdj IS '残疾等级';
COMMENT ON COLUMN dwd_zrr_jzxx_new.jtbh IS '家庭编号';
COMMENT ON COLUMN dwd_zrr_jzxx_new.tdjzdxlbmc IS '特定救助对象类别名称';
COMMENT ON COLUMN dwd_zrr_jzxx_new.dblx IS '低保类型';
COMMENT ON COLUMN dwd_zrr_jzxx_new.dbjtlqje IS '救助金额';
COMMENT ON COLUMN dwd_zrr_jzxx_new.dbjzyxzh IS '低保救助银行账号';
COMMENT ON COLUMN dwd_zrr_jzxx_new.dbjzyxmc IS '低保救助银行名称';
COMMENT ON COLUMN dwd_zrr_jzxx_new.jtzsr IS '家庭总收入';
COMMENT ON COLUMN dwd_zrr_jzxx_new.zpyy IS '致贫原因';