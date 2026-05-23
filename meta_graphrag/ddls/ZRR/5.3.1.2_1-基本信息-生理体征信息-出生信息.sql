CREATE TABLE dwd_zrr_csxx_new (
    zrrwybs VARCHAR(800),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    csyxzmbh CHAR(160),
    p_flag CHAR(160),
    csyxzmfqsfzh CHAR(144),
    csyxzmmqsfzh CHAR(144),
    csyxzmqfrq DATE,
    csyxzmqfjg VARCHAR(800),
    csdxzqhxz VARCHAR(800),
    mq_xm VARCHAR(500),
    fq_xm VARCHAR(500),
    cssj TIMESTAMP,
    csyz INTEGER,
    cstz NUMERIC,
    cssz NUMERIC,
    csd_qhdm VARCHAR(200),
    etgrbsh VARCHAR(200),
    bshlb VARCHAR(200),
    jsry VARCHAR(200),
    zcjgmc VARCHAR(400),
    xsexm VARCHAR(500),
    xsexb VARCHAR(10)
);

COMMENT ON TABLE dwd_zrr_csxx_new IS '出生信息';
COMMENT ON COLUMN dwd_zrr_csxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_csxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_csxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_csxx_new.csyxzmbh IS '出生医学证明编号';
COMMENT ON COLUMN dwd_zrr_csxx_new.p_flag IS '证照状态';
COMMENT ON COLUMN dwd_zrr_csxx_new.csyxzmfqsfzh IS '出生医学证明父亲身份证号';
COMMENT ON COLUMN dwd_zrr_csxx_new.csyxzmmqsfzh IS '出生医学证明母亲身份证号';
COMMENT ON COLUMN dwd_zrr_csxx_new.csyxzmqfrq IS '出生医学证明签发日期';
COMMENT ON COLUMN dwd_zrr_csxx_new.csyxzmqfjg IS '出生医学证明签发机构';
COMMENT ON COLUMN dwd_zrr_csxx_new.csdxzqhxz IS '出生地行政区划地址';
COMMENT ON COLUMN dwd_zrr_csxx_new.mq_xm IS '母亲姓名';
COMMENT ON COLUMN dwd_zrr_csxx_new.fq_xm IS '父亲姓名';
COMMENT ON COLUMN dwd_zrr_csxx_new.cssj IS '出生时间';
COMMENT ON COLUMN dwd_zrr_csxx_new.csyz IS '出生孕周';
COMMENT ON COLUMN dwd_zrr_csxx_new.cstz IS '出生体重';
COMMENT ON COLUMN dwd_zrr_csxx_new.cssz IS '出生身长';
COMMENT ON COLUMN dwd_zrr_csxx_new.csd_qhdm IS '出生地行政区划代码';
COMMENT ON COLUMN dwd_zrr_csxx_new.etgrbsh IS '儿童个人标识号';
COMMENT ON COLUMN dwd_zrr_csxx_new.bshlb IS '标识号类别';
COMMENT ON COLUMN dwd_zrr_csxx_new.jsry IS '接生人员';
COMMENT ON COLUMN dwd_zrr_csxx_new.zcjgmc IS '医疗机构名称';
COMMENT ON COLUMN dwd_zrr_csxx_new.xsexm IS '新生儿姓名';
COMMENT ON COLUMN dwd_zrr_csxx_new.xsexb IS '新生儿性别';