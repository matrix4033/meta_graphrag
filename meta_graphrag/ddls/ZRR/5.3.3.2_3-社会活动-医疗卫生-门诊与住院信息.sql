CREATE TABLE dwd_zrr_mzyzyxx_new (
    zrrwybs VARCHAR(1381),
    sfzjhm VARCHAR(1381),
    sfzjlx VARCHAR(1381),
    yljgdm VARCHAR(22),
    sffz VARCHAR(10),
    hzxm VARCHAR(50),
    hzsx VARCHAR(20),
    sfjz VARCHAR(1),
    jzxz VARCHAR(10),
    jzksbm VARCHAR(64),
    jzksmc VARCHAR(76),
    jzksrq DATE,
    jzsj TIMESTAMP,
    wcjzsj TIMESTAMP,
    zzysbh VARCHAR(36),
    zzysxm VARCHAR(50),
    mzzddm VARCHAR(64),
    mzzdmc VARCHAR(256),
    jzzdsm VARCHAR(512),
    zs VARCHAR(1024),
    mzzzmc VARCHAR(120),
    mzzzzddm VARCHAR(40),
    lggc VARCHAR(2),
    zzms VARCHAR(1024),
    fbrqsj DATE,
    ssy NUMERIC,
    szy NUMERIC,
    tw NUMERIC,
    zzcxsj VARCHAR(3),
    mjzh VARCHAR(36),
    jzlsh VARCHAR(36),
    jzksrq_new DATE
);

COMMENT ON TABLE dwd_zrr_mzyzyxx_new IS '门诊与住院信息';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.yljgdm IS '医疗机构代码';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.sffz IS '是否复诊';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.hzxm IS '患者姓名';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.hzsx IS '患者属性';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.sfjz IS '是否急诊';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.jzxz IS '就诊性质';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.jzksbm IS '就诊科室代码';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.jzksmc IS '就诊科室名称';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.jzksrq IS '门诊就诊日期';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.jzsj IS '接诊时间';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.wcjzsj IS '完成就诊时间';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.zzysbh IS '主诊医生编号';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.zzysxm IS '主诊医生姓名';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.mzzddm IS '门诊诊断代码';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.mzzdmc IS '门诊诊断名称（主要诊断）';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.jzzdsm IS '门诊诊断说明';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.zs IS '主诉';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.mzzzmc IS '门诊症状-名称';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.mzzzzddm IS '门诊症状-诊断代码';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.lggc IS '留观观察';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.zzms IS '症状描述';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.fbrqsj IS '发病日期时间';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.ssy IS '收缩压(mmHg)';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.szy IS '舒张压(mmHg)';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.tw IS '体温(℃)';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.zzcxsj IS '症状持续时间';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.mjzh IS '门（急）诊号';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.jzlsh IS '就诊流水号';
COMMENT ON COLUMN dwd_zrr_mzyzyxx_new.jzksrq_new IS '门诊就诊日期_new';