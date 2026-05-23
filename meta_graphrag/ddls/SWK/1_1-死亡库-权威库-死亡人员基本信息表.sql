CREATE TABLE dwd_swk_swryjbxxb_new (
    id BIGINT,
    ryid VARCHAR(64),
    zjhm VARCHAR(50),
    zjlx VARCHAR(12),
    xm_ga VARCHAR(50),
    xm_mz VARCHAR(50),
    xm_wj VARCHAR(50),
    xm_fy VARCHAR(50),
    xm_rs VARCHAR(50),
    xm_yb VARCHAR(50),
    mz VARCHAR(2),
    xb VARCHAR(1),
    GJ VARCHAR(3),
    csrq VARCHAR(8),
    fzcswbs VARCHAR(1),
    xgswbs VARCHAR(1),
    sjly VARCHAR(50),
    swcxbs VARCHAR(1),
    cybs VARCHAR(1),
    data_create_time TIMESTAMP(14)
    data_update_time TIMESTAMP(14)
);

COMMENT ON TABLE dwd_swk_swryjbxxb_new IS '死亡人员基本信息';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.id IS 'ID';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.ryid IS '自然人ID';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.zjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.zjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.xm_ga IS '姓名_公安';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.xm_mz IS '姓名_民政';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.xm_wj IS '姓名_卫健';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.xm_fy IS '姓名_法院';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.xm_rs IS '姓名_人社';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.xm_yb IS '姓名_医保';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.mz IS '民族';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.xb IS '性别';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.GJ IS '国籍';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.csrq IS '出生日期';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.fzcswbs IS '非正常死亡标识';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.xgswbs IS '宣告死亡标识';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.sjly IS '数据来源';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.swcxbs IS '死亡撤销标识';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.cybs IS '存疑标识';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.data_create_time IS '数据入库时间';
COMMENT ON COLUMN dwd_swk_swryjbxxb_new.data_update_time IS '数据变动时间';