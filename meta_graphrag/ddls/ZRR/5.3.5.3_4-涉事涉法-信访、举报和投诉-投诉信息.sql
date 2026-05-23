CREATE TABLE dwd_zrr_tsxx_new (
    zrrwybs VARCHAR(3000),
    sfzjlx CHAR(16),
    sfzjhm VARCHAR(800),
    tsr VARCHAR(255),
    tsnr VARCHAR(16000),
    tsdh VARCHAR(800),
    slssjblx CHAR(16),
    blbm VARCHAR(800),
    xzdwlx VARCHAR(160),
    xfaqsjlx TEXT,
    fkdjr VARCHAR(240)
);

COMMENT ON TABLE dwd_zrr_tsxx_new IS '投诉信息';
COMMENT ON COLUMN dwd_zrr_tsxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_tsxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_tsxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_tsxx_new.tsr IS '投诉人';
COMMENT ON COLUMN dwd_zrr_tsxx_new.tsnr IS '投诉内容';
COMMENT ON COLUMN dwd_zrr_tsxx_new.tsdh IS '投诉电话';
COMMENT ON COLUMN dwd_zrr_tsxx_new.slssjblx IS '受理申诉举报类型';
COMMENT ON COLUMN dwd_zrr_tsxx_new.blbm IS '办理部门';
COMMENT ON COLUMN dwd_zrr_tsxx_new.xzdwlx IS '协助单位类型';
COMMENT ON COLUMN dwd_zrr_tsxx_new.xfaqsjlx IS '消费安全事件类型';
COMMENT ON COLUMN dwd_zrr_tsxx_new.fkdjr IS '反馈登记人';