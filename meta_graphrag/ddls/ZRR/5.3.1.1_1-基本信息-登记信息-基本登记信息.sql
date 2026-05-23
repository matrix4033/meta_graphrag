CREATE TABLE dwd_zrr_jbdjxx_new (
    zrrwybs VARCHAR(255),
    sfzjlx VARCHAR(255),
    sfzjhm VARCHAR(255),
    xm VARCHAR(200),
    cym VARCHAR(200),
    xb VARCHAR(10),
    csrq DATE,
    mz VARCHAR(20),
    gj VARCHAR(300),
    zzmm VARCHAR(255),
    zjxy VARCHAR(20),
    byzk VARCHAR(20)
);

COMMENT ON TABLE dwd_zrr_jbdjxx_new IS '基本登记信息';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.xm IS '姓名';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.cym IS '曾用名';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.xb IS '性别';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.csrq IS '出生日期';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.mz IS '民族';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.gj IS '国籍';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.zzmm IS '政治面貌';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.zjxy IS '宗教信仰';
COMMENT ON COLUMN dwd_zrr_jbdjxx_new.byzk IS '兵役状况';