CREATE TABLE dwd_zrr_xzqz_new (
    zrrwybs VARCHAR(200),
    sfzjlx CHAR(50),
    sfzjhm VARCHAR(200),
    xzqzsqrq DATE,
    xzqzdxszzzjgtyshxydm VARCHAR(50),
    xzqzzxwh VARCHAR(100),
    xzqzfl VARCHAR(20),
    lscfsj DATE,
    cfxxxzqbm VARCHAR(50),
    xzqzzxsj DATE,
    xzqzxdrfl VARCHAR(100),
    jclscfsj TIMESTAMP,
    xzqzjfrq DATE
);

COMMENT ON TABLE dwd_zrr_xzqz_new IS '行政强制';
COMMENT ON COLUMN dwd_zrr_xzqz_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_xzqz_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_xzqz_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_xzqz_new.xzqzsqrq IS '行政强制申请日期';
COMMENT ON COLUMN dwd_zrr_xzqz_new.xzqzdxszzzjgtyshxydm IS '行政强制对象所在组织机构统一社会信用代码';
COMMENT ON COLUMN dwd_zrr_xzqz_new.xzqzzxwh IS '行政强制执行文号';
COMMENT ON COLUMN dwd_zrr_xzqz_new.xzqzfl IS '行政强制分类';
COMMENT ON COLUMN dwd_zrr_xzqz_new.lscfsj IS '临时查封时间';
COMMENT ON COLUMN dwd_zrr_xzqz_new.cfxxxzqbm IS '查封信息行政区编码';
COMMENT ON COLUMN dwd_zrr_xzqz_new.xzqzzxsj IS '行政强制执行时间';
COMMENT ON COLUMN dwd_zrr_xzqz_new.xzqzxdrfl IS '行政强制相对人分类';
COMMENT ON COLUMN dwd_zrr_xzqz_new.jclscfsj IS '解除临时查封时间';
COMMENT ON COLUMN dwd_zrr_xzqz_new.xzqzjfrq IS '行政强制解封日期';