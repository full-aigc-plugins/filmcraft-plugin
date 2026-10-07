# 多机位访谈剪辑 / Multi-camera interview editing

适用于已有多个同步机位的访谈、演讲或演出，按时间切换画面，并保留指定主录音。此手册使用真实 `multicam.*` 参数合同；不把目录存在当成同步、剪辑或导出已成功。

Use this workflow for synchronized interview, presentation or performance angles with an explicitly selected audio policy. Query the current project before choosing camera indices.

## 输入与同步边界 / Inputs and synchronization

- 输入每个机位素材、主录音、目标序列和切换时间；确认帧率、素材起点及同步依据。已有多机位序列先读取实际角度顺序、选中片段和播放头。
- 不将导入的多个普通片段自动视为已同步多机位。缺少同步依据时先完成同步并检查共同事件的音画位置；本手册不虚构自动同步参数。
- `camera` 是显示顺序的 1–16；`angle` 从 0 开始。每次从当前序列核对，不使用例子中的角度代替用户工程。
- `time` 使用 ticks，每秒 254016000000；原生命令的 ticks 参数使用精确 JSON 整数；不要向本例的原生 time 参数传数字字符串，否则可能被忽略并回退播放头。可用 playhead.set 的 seconds 参数显式定位。

Provide real angle media, a master audio source, a target sequence and cut times. Confirm frame rates and synchronization against a shared event. Imported clips alone do not establish synchronization. Camera numbers are 1-based display positions; angles are 0-based.

## 选择操作 / Choose the operation

| 请求 / Request | 命令 / Command | 关键区别 / Decision |
| --- | --- | --- |
| 调整机位名称与可用状态 | `multicam.editCameras` | 查询 `sequence`；`cameras` 中的 `angle` 为 0-based，音频政策按真实 `camera1\|all\|switch` 合同选择 |
| 改变已有片段的角度 | `multicam.switchAngle` | 可以提供实际 `clips`；先明确是改视频、音频还是两者 |
| 在指定时间切换并产生切点 | `multicam.cutToCamera` / `multicam.cut` | 区别于仅替换当前角度；检查产生的时间线边界 |
| 保持主录音连续 | `multicam.audioFollowsVideo` | 根据用户目标设置 `enabled`，并检查输出音轨；关闭跟随不等于主录音已经正确选择 |
| 实时录制切换 | `multicam.recordStart` / `multicam.recordStop` | 同一会话配对；中断时先查询录制状态，不能直接重放开始命令 |
| 查看更多机位 | `multicam.gridLayout` / `multicam.page` / `multicam.nextPage` | 视图布局和分页不等于成片中的切换 |

Read `command-reference.md` for exact native parameters. View changes do not prove timeline edits; switching an existing angle and inserting a cut have different acceptance checks.

## 参数查询与执行 / Describe and execute

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" list --filter multicam.
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.editCameras
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.audioFollowsVideo
```

按本技能 `command-usage.md` 的 `craft-command-plan/v1` 合同构造计划；原生参数放入对应命令步骤，不将本表直接当作可执行 JSON。打开同步序列、读取对象、选择目标片段后重新查询 enabled；禁用时报告实际上下文和原因。完成 `check` 后以新输出目录执行 `run`，在同一原生会话保存新的 `.fcproj`。

Build a command plan using the local gateway contract. Re-query command availability after opening and selecting the synchronized sequence. Save in the same native session; use a new delivery location.

## 局部修改与交付 / Revision and delivery

修改一个切点时记录原切点、相邻片段和主音轨摘要；只修改目标切点或角度。交付新 `.fcproj`、引用素材清单、预览与成片。重开工程核对角度和切点；解码目标切点前后的视频帧，检查主录音连续、音画同步和非目标片段未改变。保留原工程与原交付。

On revision, compare the target cut, adjacent clips and master audio before and after. Reopen the native project and inspect decoded frames around the cut. Confirm continuous audio and unchanged unrelated content. This guide remains pending real multi-camera execution acceptance.

## 已执行代表实例 / Executed representative example

`examples/multicam-create.json` 接收 `--input red=/absolute/camera1.mp4 --input blue=/absolute/camera2.mp4`，显式 project.select 选择素材后建立 in-point 同步序列，以 camera1 为主录音，在1秒播放头做 videoOnly 切换。样例素材是96×64、12fps、两秒，必须适配真实素材同步依据。`examples/multicam-reopen.json` 接收 `--input project=/absolute/project.fcproj`；其中成片序列ID16只适用于本例，真实项目先查询实际序列ID并修改该步骤。重开可能默认激活源序列，必须显式 sequence.open 成片序列再检查和导出。两例使用本技能 commands.py run 和新输出目录。

已核验两个视频片段、一个连续音频片段、重开音轨一致，成片0.5秒红色与1.5秒蓝色，两个片段均保留440Hz主录音；不代表全部多机位命令已验收。

The bounded example explicitly selects imported project items, sets the playhead in seconds and reopens the actual final sequence. Adapt the fixture-only sequence ID and sync assumptions. Decoded video switches cameras while master audio remains continuous.
