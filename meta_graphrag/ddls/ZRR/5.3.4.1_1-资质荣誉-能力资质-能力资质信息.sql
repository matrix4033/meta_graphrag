CREATE TABLE dwd_zrr_nlzzxx_new (
    zrrwybs VARCHAR(1600),
    sfzjlx CHAR(400),
    sfzjhm VARCHAR(1600),
    zsbh VARCHAR(2400),
    zzdj VARCHAR(2400),
    zjyxqq DATE,
    zjyxqz DATE,
    zjqfjgmc VARCHAR(640),
    fzjg VARCHAR(1280),
    zjqfrq VARCHAR(1280),
    zjbh VARCHAR(1920),
    bajgdm VARCHAR(1280),
    bajgmc VARCHAR(1280),
    sfscxdzsh VARCHAR(1280),
    zt VARCHAR(1280),
    cd_batch VARCHAR(1280),
    cyfw VARCHAR(1280),
    zjmc VARCHAR(2400),
    qhdm VARCHAR(2560),
    zjqmz VARCHAR(400),
    zzjtm VARCHAR(400),
    zjqmgyz VARCHAR(400),
    zjqmhashz VARCHAR(400),
    zjqfjgdm VARCHAR(400),
    zjccqfrq DATE,
    zjzxrq DATE,
    zjzxyy VARCHAR(800),
    zjlx VARCHAR(96),
    zjsjc DATE
);

COMMENT ON TABLE dwd_zrr_nlzzxx_new IS '能力资质信息';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zrrwybs IS '自然人唯一标识';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.sfzjlx IS '身份证件类型';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.sfzjhm IS '身份证件号码';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zsbh IS '证书编号-弃用';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zzdj IS '资质等级';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjyxqq IS '证件有效期起';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjyxqz IS '证件有效期止';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjqfjgmc IS '证件签发机关名称';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.fzjg IS '发证机关-弃用';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjqfrq IS '证件签发日期';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjbh IS '证件编号';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.bajgdm IS '备案机构代码';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.bajgmc IS '备案机构名称';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.sfscxdzsh IS '是否生成新的证书号';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zt IS '状态';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.cd_batch IS '批次号';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.cyfw IS '从业范围';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjmc IS '证件名称';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.qhdm IS '区划代码';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjqmz IS '证件签名值';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zzjtm IS '证件条码';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjqmgyz IS '证件签名公钥值';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjqmhashz IS '证件签名hash值';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjqfjgdm IS '证件签发机关代码';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjccqfrq IS '证件初次签发日期';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjzxrq IS '证件注销日期';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjzxyy IS '证件注销原因';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjlx IS '证件类型';
COMMENT ON COLUMN dwd_zrr_nlzzxx_new.zjsjc IS '证件时间戳';