# 完整原生命令参考 / Complete native command reference

本参考逐项保留锁定参数原文与技能路由。命令执行必须满足当前工程、选择对象、素材或 GUI 前置状态。
This reference preserves each pinned parameter contract and skill owner. Query live state before invocation.

使用方法见 [完整调用指南](command-usage.md)。全部参数均为原生语法说明，不把它们假装成 JSON Schema。
每项 NOT_RUN 指本轮完整逐命令验收；既有代表任务证据仍单独保留。

## file.newProject

Project…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newProject`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str}
```

## file.openDemoProject

Demo Project

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.openDemoProject`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.newSequence

Sequence…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newSequence`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"width":u32=1920,"height":u32=1080,"fps":f64=23.976,"sampleRate":u32=48000,"video":n=3,"audio":n=3,"mix":"Stereo|Mono|5.1|Adaptive"?,"trackType":"Standard|Mono|5.1|Adaptive"?,"fromItem":itemId?}
```

## file.newSequenceFromClip

Sequence From Clip

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newSequenceFromClip`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## file.newBin

Bin

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newBin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"parent":binId?}
```

## file.newBinFromSelection

Bin From Selection

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newBinFromSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"name":str?}
```

## file.newSearchBin

Search Bin

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newSearchBin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"column":str?,"operator":str?,"text":str?,"rows":[..]?,"matchAll":bool?,"caseSensitive":bool?}
```

## file.newOfflineFile

Offline File…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newOfflineFile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"fileName":str?,"tapeName":str?,"video":bool=true,"audio":bool=true,"width":u32?,"height":u32?,"fps":f64?,"sampleRate":u32=48000,"channels":u32=2,"timecode":"HH:MM:SS:FF"?,"seconds":f64=10,"description":str?}
```

## file.newAdjustmentLayer

Adjustment Layer…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newAdjustmentLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"seconds":f64=5}
```

## file.newBarsAndTone

Bars and Tone…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newBarsAndTone`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"seconds":f64=10}
```

## file.newBlackVideo

Black Video…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newBlackVideo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"seconds":f64}
```

## file.newColorMatte

Color Matte…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newColorMatte`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":"#rrggbb","seconds":f64}
```

## file.newCountingLeader

Universal Counting Leader…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newCountingLeader`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.newTransparentVideo

Transparent Video…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newTransparentVideo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.importDemoFootage

Demo Footage

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.importDemoFootage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"scene":"OceanSunset|Aurora|CityNight|Dunes|Plasma|Forest"}
```

## file.exportInterchange

Export Interchange

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportInterchange`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"format":"edl|xml|fcpxml|otio","path":str,"sequence":id?}
```

## file.exportEdl

EDL…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportEdl`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.exportSelectionProject

Selection as FilmCraft Project…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportSelectionProject`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"items":[id]?}
```

## file.exportAle

Avid Log Exchange…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportAle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"items":[id]?}
```

## file.exportOtio

OpenTimelineIO…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportOtio`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.exportFcp7Xml

Final Cut Pro XML…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportFcp7Xml`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.exportFcpxml

FCPXML…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportFcpxml`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.exportAaf

AAF…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportAaf`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"sequence":id?,"mixdownVideo":bool?,"mixdownFormat":"mov|mxf"?,"breakoutToMono":bool?,"audio":"embedded|separate|linked"?,"audioFormat":"wav|aiff|mxf"?,"sampleRate":int?,"bitDepth":"16|24"?,"trimAudio":bool?,"handles":frames?,"renderAudioEffects":bool?,"smallSectors":bool?}
```

## file.exportOmf

OMF…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportOmf`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"sequence":id?,"title":str?,"audio":"embedded|separate"?,"audioFormat":"wav|aiff"?,"sampleRate":int?,"bitDepth":"16|24"?,"trimAudio":bool?,"handles":frames?,"renderAudioEffects":bool?,"breakoutToMono":bool?}
```

## file.importAaf

Import AAF…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.importAaf`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.open

Open Project…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.open`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.close

Close

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.close`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?}
```

## file.closeProject

Close Project

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.closeProject`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"force":bool?}
```

## file.closeAllProjects

Close All Projects

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.closeAllProjects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"force":bool?}
```

## file.closeAllOtherProjects

Close All Other Projects

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.closeAllOtherProjects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.save

Save

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str?}
```

## file.saveAs

Save As…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.saveAs`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.saveCopy

Save a Copy…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.saveCopy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.saveAsTemplate

Save as Template…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.saveAsTemplate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"path":str?}
```

## file.saveAll

Save All

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.saveAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.revert

Revert

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.revert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.recover

Recover Unsaved Changes…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.recover`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":str?}
```

## file.discardRecovery

Discard Unsaved Changes

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.discardRecovery`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":str?,"all":bool?}
```

## file.recoveryList

List Recoverable Sessions

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.recoveryList`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.autoSaveNow

Auto Save Now

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.autoSaveNow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.autoSaveStatus

Auto Save Status

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.autoSaveStatus`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.listAutoSaves

Browse Auto-Saves

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.listAutoSaves`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## prefs.get

Get Preferences

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"key":str?}
```

## prefs.set

Set Preferences

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"key":str,"value":any}|{"values":{key:value}}
```

## prefs.reset

Reset Preferences

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"category":str?}
```

## file.exportMedia

Media…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportMedia`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"preset":str?,"settings":ExportSettings?,"format":"h264|prores|dnxhr|mjpeg|mxf-op1a|mxf-opatom|png|tiff|bmp|gif|wav|aiff"?,"width":u32?,"height":u32?,"fps":f64?,"bitrateKbps":u32?,"bitrateMode":"cbr|vbr1Pass|vbr2Pass"?,"scale":f32=1,"audio":bool=true,"quality":0..100,"burnCaptions":bool=false,"captionSidecar":"srt|vtt"?,"loudnessLufs":f64?,"proresProfile":"proxy|lt|standard|hq"?,"dnxProfile":"lb|sq|hq|hqx"?,"mxfVideoCodec":"dnxhr|proRes|h264"?,"sequence":id?,"range":"entire|inOut|workArea|custom"?,"startSeconds":f64?,"endSeconds":f64?,"wait":bool=false}
```

## jobs.list

List Jobs

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe jobs.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## perf.stats

Performance Statistics

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe perf.stats`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## jobs.cancel

Cancel Job

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe jobs.cancel`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"job":id}
```

## edit.undo

Undo

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.undo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.redo

Redo

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.redo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.cut

Cut

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.cut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.copy

Copy

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.copy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.paste

Paste

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.paste`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.pasteInsert

Paste Insert

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteInsert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.pasteAttributes

Paste Attributes…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteAttributes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"motion":bool=true,"opacity":bool=true,"timeRemapping":bool=true,"volume":bool=true,"channelVolume":bool=true,"panner":bool=true,"effects":bool|[effectId]=true,"scaleTimes":bool=true}
```

## edit.removeAttributes

Remove Attributes…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.removeAttributes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"motion":bool=true,"opacity":bool=true,"timeRemapping":bool=true,"volume":bool=true,"channelVolume":bool=true,"panner":bool=true,"effects":bool|[effectId]=true}
```

## edit.clear

Clear

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## edit.rippleDelete

Ripple Delete

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.rippleDelete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## edit.selectAll

Select All

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.selectAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.selectAllMatching

Select All Matching

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.selectAllMatching`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## edit.deselectAll

Deselect All

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.deselectAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.find

Find…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.find`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"scope":"project|timeline"?,"column":str?,"operator":"contains|matches|beginsWith|endsWith|doesNotContain"?,"text":str?,"rows":[{"column":str,"operator":str,"text":str}]?,"matchAll":bool=true,"caseSensitive":bool=false,"in":"all|clips|markers"?}
```

## edit.findNext

Find Next

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.findNext`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.duplicate

Duplicate

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.selectLabelGroup

Select Label Group

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.selectLabelGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.label.violet

Violet

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.violet`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.iris

Iris

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.iris`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.caribbean

Caribbean

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.caribbean`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.lavender

Lavender

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.lavender`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.cerulean

Cerulean

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.cerulean`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.forest

Forest

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.forest`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.rose

Rose

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.rose`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.mango

Mango

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.mango`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.purple

Purple

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.purple`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.blue

Blue

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.blue`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.teal

Teal

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.teal`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.magenta

Magenta

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.magenta`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.tan

Tan

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.tan`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.green

Green

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.green`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.brown

Brown

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.brown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.label.yellow

Yellow

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label.yellow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"clips":[id]?}
```

## edit.removeUnused

Remove Unused

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.removeUnused`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.consolidateDuplicates

Consolidate Duplicates

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.consolidateDuplicates`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.editOriginal

Edit Original

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.editOriginal`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## edit.label

Label

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.label`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"label":"Violet|Iris|…"}
```

## clip.rename

Rename…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"item":id?,"name":str}
```

## clip.makeSubclip

Make Subclip…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.makeSubclip`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?,"clip":id?,"name":str?,"start":ticks?,"end":ticks?,"startFrame":i64?,"endFrame":i64?,"restrictTrims":bool=true}
```

## clip.editSubclip

Edit Subclip…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.editSubclip`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?,"start":ticks?,"end":ticks?,"startFrame":i64?,"endFrame":i64?,"restrictTrims":bool?,"convertToMaster":bool?}
```

## clip.editOffline

Edit Offline…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.editOffline`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?,"mediaName":str?,"tapeName":str?,"description":str?,"scene":str?,"shot":str?,"logNote":str?}
```

## clip.sourceSettings

Source Settings…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.sourceSettings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?}
```

## clip.audioChannels

Audio Channels…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.audioChannels`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"format":"mono|stereo|5.1|adaptive","clips":[[channel]]?,"channels":[channel]?}
```

## clip.interpretFootage

Interpret Footage…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.interpretFootage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"colorSpace":"auto"|"<color space id>"}
```

## clip.modifyTimecode

Timecode…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.modifyTimecode`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?,"timecode":"HH:MM:SS:FF"?,"frame":i64?,"tapeName":str?,"reset":bool?}
```

## clip.frameHoldOptions

Frame Hold Options…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.frameHoldOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"enabled":bool=true,"holdOn":"sourceTimecode|sequenceTime|in|out|playhead","time":ticks?,"timecode":str?,"holdFilters":bool=false}
```

## clip.frameHold

Add Frame Hold

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.frameHold`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"time":ticks?}
```

## clip.insertFrameHoldSegment

Insert Frame Hold Segment

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.insertFrameHoldSegment`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"time":ticks?,"seconds":f64=2}
```

## clip.fieldOptions

Field Options…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.fieldOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"reverseFieldDominance":bool=false,"processing":"none|alwaysDeinterlace|flickerRemoval"}
```

## clip.timeInterpolation.frameSampling

Frame Sampling

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.timeInterpolation.frameSampling`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.timeInterpolation.frameBlending

Frame Blending

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.timeInterpolation.frameBlending`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.timeInterpolation.opticalFlow

Optical Flow

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.timeInterpolation.opticalFlow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.scaleToFrameSize

Scale to Frame Size

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.scaleToFrameSize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.fitToFrame

Fit to frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.fitToFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.fillFrame

Fill frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.fillFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.audioGain

Audio Gain…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.audioGain`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"mode":"set|adjust|normalizeMax|normalizeAll"?,"db":f64,"relative":bool?}
```

## clip.breakoutToMono

Breakout to Mono

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.breakoutToMono`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## clip.extractAudio

Extract Audio

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.extractAudio`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"dir":str?}
```

## clip.speedDuration

Speed/Duration…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.speedDuration`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"speed":percent=100,"reverse":bool,"ripple":bool,"interpolation":"frameSampling|frameBlending|opticalFlow"?}
```

## clip.sceneEditDetection

Scene Edit Detection…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.sceneEditDetection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"sensitivity":0..100=50,"minShotFrames":n=6,"applyCuts":bool=true,"createSubclips":bool=false,"generateMarkers":bool=false,"wait":bool=false}
```

## clip.enable

Enable

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.enable`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.link

Link

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.link`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.group

Group

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.group`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.ungroup

Ungroup

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.ungroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.audioPeak

Audio Clip Peak Amplitude

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.audioPeak`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.nest

Nest…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.nest`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str}
```

## sequence.open

Open in Timeline

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.open`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id}
```

## sequence.close

Close Sequence

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.close`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?}
```

## sequence.settings

Sequence Settings…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.settings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"width":u32?,"height":u32?,"fps":f64?,"name":str?,"sampleRate":u32?,"mix":"Stereo|Mono|5.1|Adaptive"?}
```

## sequence.renderEffectsInToOut

Render Effects In to Out

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.renderEffectsInToOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"wait":bool=false}
```

## sequence.renderInToOut

Render In to Out

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.renderInToOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"wait":bool=false}
```

## sequence.renderSelection

Render Selection

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.renderSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"wait":bool=false}
```

## sequence.renderAudio

Render Audio

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.renderAudio`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"wait":bool=false}
```

## sequence.deleteRenderFiles

Delete Render Files

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.deleteRenderFiles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.deleteRenderFilesInToOut

Delete Render Files In to Out

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.deleteRenderFilesInToOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.matchFrame

Match Frame

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.matchFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.reverseMatchFrame

Reverse Match Frame

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.reverseMatchFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.addEdit

Add Edit

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.addEdit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## sequence.addEditAllTracks

Add Edit to All Tracks

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.addEditAllTracks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## trim.edit

Trim Edit

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.applyVideoTransition

Apply Video Transition

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.applyVideoTransition`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":"cross_dissolve|Cross Dissolve|…"?,"frames":i64?,"edge":"in"|"out"?,"params":{param:value}?,"reverse":bool?}
```

## sequence.applyAudioTransition

Apply Audio Transition

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.applyAudioTransition`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":str?,"frames":i64?}
```

## trim.applyDefaultTransition

Apply Default Transitions to Selection

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.applyDefaultTransition`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## sequence.lift

Lift

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.lift`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.extract

Extract

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.extract`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.closeGap

Close Gap

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.closeGap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"V1"|id,"time":ticks}
```

## sequence.goToNextGap

Next in Sequence

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.goToNextGap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.goToPrevGap

Previous in Sequence

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.goToPrevGap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.goToNextGapInTrack

Next in Track

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.goToNextGapInTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"V1"|id?}
```

## sequence.goToPrevGapInTrack

Previous in Track

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.goToPrevGapInTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"V1"|id?}
```

## sequence.snap

Snap in Timeline

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.snap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool?}
```

## sequence.linkedSelection

Linked Selection

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.linkedSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool?}
```

## sequence.selectionFollowsPlayhead

Selection Follows Playhead

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.selectionFollowsPlayhead`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool?}
```

## sequence.showThroughEdits

Show Through Edits

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.showThroughEdits`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool?}
```

## sequence.normalizeMixTrack

Normalize Mix Track…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.normalizeMixTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"db":f64=0}
```

## sequence.makeSubsequence

Make Subsequence

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.makeSubsequence`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?}
```

## sequence.transcribe

Transcribe Sequence…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.transcribe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"mix"|"A1"|id?,"language":"en|auto"?,"diarize":bool?,"maxSpeakers":n?,"model":str?}
```

## sequence.simplify

Simplify Sequence…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.simplify`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"removeDisabled":bool=true,"removeEmptyTracks":bool=true,"closeGaps":bool=false,"moveClipsDown":bool=false,"removeVideoEffects":bool=false,"removeAudioEffects":bool=false,"removeText":bool=false,"keep":"both|video|audio"}
```

## sequence.addTracks

Add Tracks…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.addTracks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"video":n=1,"audio":n=0}
```

## sequence.deleteTracks

Delete Tracks…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.deleteTracks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"video":"empty"|"V2"|id?,"audio":"empty"|"A2"|id?}
```

## sequence.colorSettings

Color Management…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.colorSettings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"workingSpace":"rec709"|"rec2100-pq"|"rec2100-hlg"?,"wideGamut":bool?,"autoToneMap":bool?}
```

## mixer.addSubmix

Add Audio Submix Track

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.addSubmix`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"channels":"Mono|Stereo|5.1"?}
```

## sequence.setTransition

Edit Transition Settings

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.setTransition`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"transition":id,"params":{param:value}?,"reverse":bool?,"reset":bool?}
```

## sequence.joinThroughEdits

Join Through Edits

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.joinThroughEdits`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"all":bool?}
```

## sequence.throughEdits

List Through Edits

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.throughEdits`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.deleteTrack

Delete Track

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.deleteTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"V3"|id}
```

## sequence.renderBar

Render Bar

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.renderBar`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.markIn

Mark In

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.markIn`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"target":"program|source"}
```

## markers.markOut

Mark Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.markOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"target":"program|source"}
```

## markers.markClip

Mark Clip

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.markClip`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.markSelection

Mark Selection

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.markSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.markSplitVideoIn

Video In

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.markSplitVideoIn`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"target":"program|source"}
```

## markers.markSplitVideoOut

Video Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.markSplitVideoOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"target":"program|source"}
```

## markers.markSplitAudioIn

Audio In

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.markSplitAudioIn`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"target":"program|source"}
```

## markers.markSplitAudioOut

Audio Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.markSplitAudioOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"target":"program|source"}
```

## markers.goToIn

Go to In

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.goToIn`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.goToOut

Go to Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.goToOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.goToSplitVideoIn

Video In

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.goToSplitVideoIn`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"target":"program|source"}
```

## markers.goToSplitVideoOut

Video Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.goToSplitVideoOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"target":"program|source"}
```

## markers.goToSplitAudioIn

Audio In

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.goToSplitAudioIn`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"target":"program|source"}
```

## markers.goToSplitAudioOut

Audio Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.goToSplitAudioOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"target":"program|source"}
```

## markers.clearIn

Clear In

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.clearIn`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.clearOut

Clear Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.clearOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.clearInOut

Clear In and Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.clearInOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.add

Add Marker

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"name":str?,"comment":str?,"color":label?,"durationFrames":i64?}
```

## markers.addRange

Add Range Marker

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.addRange`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"durationFrames":i64=1s,"duration":ticks?,"name":str?,"comment":str?,"color":label?}
```

## markers.addRangeInOut

Add Range Marker to In and Out

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.addRangeInOut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"comment":str?,"color":label?}
```

## markers.goNext

Go to Next Marker

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.goNext`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.goPrev

Go to Previous Marker

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.goPrev`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.clearCurrent

Clear Selected Marker

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.clearCurrent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.clearAll

Clear Markers

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.clearAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.showAllMarkerColors

Show All Marker Colors

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.showAllMarkerColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## markers.filterColors

Marker Colour Filter

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.filterColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"hidden":[label]}|{"color":label,"visible":bool?}
```

## markers.edit

Edit Marker…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"marker":id,"name":str?,"comment":str?,"color":label?,"durationFrames":i64?}
```

## markers.addChapter

Add Chapter Marker…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.addChapter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"name":str?,"comment":str?,"color":label?}
```

## markers.addFlashCue

Add Flash Cue Marker…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.addFlashCue`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"name":str?,"comment":str?,"color":label?}
```

## markers.rippleSequenceMarkers

Ripple Sequence Markers

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.rippleSequenceMarkers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool?}
```

## markers.copyPasteIncludesSequenceMarkers

Copy Paste Includes Sequence Markers

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe markers.copyPasteIncludesSequenceMarkers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool?}
```

## playhead.set

Set Playhead

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks|"frame":i64|"seconds":f64|"timecode":str}
```

## playhead.step

Step Frames

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.step`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"frames":i64}
```

## playhead.stepForward

Step Forward One Frame

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.stepForward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.stepBack

Step Back One Frame

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.stepBack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.stepForward5

Step Forward Five Frames

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.stepForward5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.stepBack5

Step Back Five Frames

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.stepBack5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.nextEdit

Go to Next Edit Point

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.nextEdit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.prevEdit

Go to Previous Edit Point

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.prevEdit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.start

Go to Sequence Start

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.start`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.end

Go to Sequence End

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.end`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## source.open

Open in Source Monitor

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe source.open`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?}
```

## source.setPlayhead

Set Source Playhead

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe source.setPlayhead`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks|"frame":i64|"seconds":f64}
```

## source.inspect

Inspect Source Monitor

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe source.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## source.insert

Insert

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe source.insert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## source.overwrite

Overwrite

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe source.overwrite`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.replaceFromSource

From Source Monitor

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.replaceFromSource`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.replaceFromSourceMatchFrame

From Source Monitor, Match Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.replaceFromSourceMatchFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## clip.replaceFromBin

From Bin

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.replaceFromBin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"item":id?}
```

## clip.restoreCaptionsFromSource

Restore Captions from Source Clip

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.restoreCaptionsFromSource`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.updateMetadata

Update Metadata…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.updateMetadata`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## clip.generateAudioWaveform

Generate Audio Waveform

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.generateAudioWaveform`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## clip.automateToSequence

Automate to Sequence…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.automateToSequence`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"ordering":"sort|selection","placement":"sequentially|unnumberedMarkers","method":"insert|overwrite","overlapFrames":n=30,"stillFrames":n?,"videoTransition":bool=true,"audioTransition":bool=true,"ignoreAudio":bool=false,"ignoreVideo":bool=false}
```

## timeline.place

Place Clip

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.place`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id,"track":"V1"|id?,"audioTrack":"A1"|id?,"time":ticks|"frame":i64|"seconds":f64,"insert":bool,"sourceIn":ticks?,"duration":ticks?}
```

## timeline.select

Select Clips

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id],"add":bool,"toggle":bool}
```

## timeline.move

Move Clips

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"moves":[{"clip":id,"track":id|"V2","time":ticks}],"insert":bool}
```

## timeline.trim

Trim Edit

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.trim`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"edge":"in|out","mode":"regular|ripple","delta":ticks|"deltaFrames":i64}
```

## trim.selectEditPoint

Select Edit Point

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.selectEditPoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"edge":"in|out","kind":"trim|ripple|roll","add":bool?}
```

## trim.selectNearest

Select Nearest Edit Point

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.selectNearest`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"kind":"rippleIn|rippleOut|roll|trimIn|trimOut"}
```

## trim.clear

Clear Edit Point Selection

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.toggleType

Toggle Trim Type

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.toggleType`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.backward

Trim Backward

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.backward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.forward

Trim Forward

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.forward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.backwardMany

Trim Backward Many

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.backwardMany`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.forwardMany

Trim Forward Many

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.forwardMany`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.shuttle

Dynamic Trim (Shuttle)

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.shuttle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"direction":"forward|reverse","slow":bool?,"clock":seconds}
```

## trim.shuttleStop

Dynamic Trim Stop

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.shuttleStop`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clock":seconds?}
```

## trim.cancelDynamic

Cancel Dynamic Trim

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.cancelDynamic`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.playAround

Play Around Edit

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.playAround`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clock":seconds,"loop":bool=true,"toggle":bool?}
```

## trim.tick

Advance Trim Playback

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.tick`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clock":seconds}
```

## trim.monitor

Trim Monitor State

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.monitor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.nudge

Trim by Frames

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.nudge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"frames":i64}
```

## trim.extendToPlayhead

Extend Selected Edit to Playhead

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.extendToPlayhead`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.ripplePrevious

Ripple Trim Previous Edit to Playhead

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.ripplePrevious`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.rippleNext

Ripple Trim Next Edit to Playhead

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.rippleNext`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.previous

Trim Previous Edit to Playhead

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.previous`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.next

Trim Next Edit to Playhead

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.next`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.roll

Rolling Edit

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.roll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"left":id,"right":id,"delta":ticks|"deltaFrames":i64}
```

## timeline.slip

Slip

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slip`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"delta":ticks|"deltaFrames":i64}
```

## timeline.slide

Slide

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"delta":ticks|"deltaFrames":i64}
```

## timeline.rateStretch

Rate Stretch

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.rateStretch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"edge":"in|out","delta":ticks}
```

## timeline.razor

Razor

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.razor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks,"track":"V1"|id?,"clip":id?}
```

## timeline.setTrack

Track Settings

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.setTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"V1"|id,"locked":bool?,"syncLock":bool?,"enabled":bool?,"muted":bool?,"solo":bool?,"name":str?,"volumeDb":f64?,"pan":f64?}
```

## timeline.setTargeting

Track Targeting

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.setTargeting`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"V1"|id,"targeted":bool?,"sourcePatch":bool?}
```

## effects.apply

Apply Effect

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"effect":"gaussian_blur|Gaussian Blur|…"}
```

## effects.remove

Remove Effect

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"index":n}
```

## effects.setParam

Set Effect Parameter

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.setParam`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":"motion"|index,"param":str,"mask":n?,"value":num|[x,y]|"#rrggbb"|bool|path,"time":ticks?}
```

## effects.toggleAnimation

Toggle Animation

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.toggleAnimation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":str|index,"param":str,"mask":n?}
```

## effects.toggleEnabled

Toggle Effect

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.toggleEnabled`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"index":n}
```

## effects.reset

Reset Effect

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"index":n}
```

## effects.addKeyframe

Add/Remove Keyframe

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.addKeyframe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":str|index,"param":str,"mask":n?,"time":ticks?}
```

## effects.deleteKeyframe

Delete Keyframe

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.deleteKeyframe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":str|index,"param":str,"mediaTime":ticks}
```

## effects.moveKeyframe

Move Keyframe

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.moveKeyframe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":str|index,"param":str,"mediaTime":ticks,"to":ticks}
```

## effects.setInterpolation

Keyframe Interpolation

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.setInterpolation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":str|index,"param":str,"mediaTime":ticks,"interpolation":"linear|bezier|autoBezier|continuousBezier|hold|easeIn|easeOut"}
```

## effects.setKeyframe

Edit Keyframe

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.setKeyframe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":str|index,"param":str,"mediaTime":ticks,"value":any?,"inInfluence":0..1?,"outInfluence":0..1?}
```

## project.select

Select Project Items

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]}
```

## project.delete

Clear

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## project.moveToBin

Move to Bin

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.moveToBin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"bin":binId|null}
```

## project.setMarks

Set Source In/Out

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.setMarks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id,"in":ticks?|null,"out":ticks?|null}
```

## command.list

List Commands

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe command.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## project.inspect

Inspect Project

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.inspect

Inspect Sequence

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?}
```

## state.inspect

Inspect Editor State

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe state.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## effects.list

List Effects

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"kind":"Video"|"Audio"|"VideoTransition"|"AudioTransition"?,"folder":"Video Transitions/Wipe"?,"detail":bool?}
```

## history.list

List History

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe history.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## captions.newTrack

Add New Caption Track…

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.newTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"format":"Subtitle|CEA-608|CEA-708|Teletext","name":str?,"language":str?}
```

## captions.deleteTrack

Delete Caption Track

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.deleteTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":id|"C1"}
```

## captions.setTrack

Caption Track Settings

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.setTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":id|"C1","name":str?,"format":str?,"language":str?,"enabled":bool?,"locked":bool?,"syncLock":bool?}
```

## captions.setStyle

Caption Track Style

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.setStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":id|"C1","font":str?,"size":f32?,"color":"#rrggbb[aa]"?,"background":bool?,"backgroundColor":"#rrggbbaa"?,"align":"left|center|right"?,"anchor":"top|middle|bottom"?,"margin":0..0.45 (fraction of frame height)?,"lineSpacing":f32?,"outline":f32?,"outlineColor":str?,"reset":bool?}
```

## captions.add

Add Caption at Playhead

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":id|"C1"?,"text":str?,"time":ticks?,"seconds":f64?,"durationSeconds":f64=3}
```

## captions.split

Split Caption

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.split`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"caption":id?,"time":ticks?}
```

## captions.merge

Merge Captions

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.merge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"captions":[id]?}
```

## captions.setText

Edit Caption Text

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.setText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"caption":id?,"text":str?,"speaker":str|null?}
```

## captions.setTimes

Set Caption In/Out

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.setTimes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"caption":id?,"startTime|startFrame|startSeconds|startTimecode":…,"endTime|endFrame|endSeconds|endTimecode":…}
```

## captions.trim

Trim Caption

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.trim`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"caption":id,"edge":"in|out","delta":ticks|"deltaFrames":i64}
```

## captions.move

Move Captions

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"captions":[id]?,"delta":ticks|"deltaFrames":i64}
```

## captions.delete

Delete Captions

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"captions":[id]?,"ripple":bool=false}
```

## captions.select

Select Captions

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"captions":[id],"add":bool?}
```

## captions.goTo

Go to Caption

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.goTo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"caption":id}
```

## captions.next

Go to Next Caption Segment

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.next`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## captions.previous

Go to Previous Caption Segment

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.previous`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## captions.showAll

Show All Caption Tracks

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.showAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## captions.showActiveOnly

Show Active Caption Tracks Only

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.showActiveOnly`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":id|"C1"?}
```

## captions.hideAll

Hide All Caption Tracks

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.hideAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## captions.import

Import Captions…

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"name":str?}
```

## captions.export

Captions…

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"format":"srt|vtt|scc|mcc|stl|ttml|dfxp"? (default: from the extension),"track":id|"C1"?,"dropFrame":bool=true}
```

## captions.list

List Captions

- 技能 / Owner: `filmcraft-cli-subtitles`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-subtitles`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe captions.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":id|"C1"?}
```

## prefs.schema

Settings Schema

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.schema`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"category":str?}
```

## mediaCache.info

Media Cache Info

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaCache.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## mediaCache.clean

Delete Media Cache Files

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaCache.clean`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"all":bool?}
```

## mixer.inspect

Inspect Audio Track Mixer

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## mixer.setStrip

Track Mixer Settings

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.setStrip`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"name":str?,"volumeDb":f64?,"pan":f64?,"muted":bool?,"solo":bool?,"recordArm":bool?,"soloSafe":bool?,"mode":"Off|Read|Latch|Touch|Write"?,"output":"Mix"|"S1"?,"inputMap":"Stereo|Left|Right|Swap|Mono"?,"channels":"Mono|Stereo|5.1"?}
```

## mixer.setValue

Set Mixer Control

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.setValue`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"lane":"volume|pan|mute|send.<i>.level|fx.<slot>.<param>","value":f64,"time":ticks?}
```

## mixer.touch

Touch Mixer Control

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.touch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"lane":"volume|pan|mute|send.<i>.level|fx.<slot>.<param>","value":f64,"time":ticks?}
```

## mixer.release

Release Mixer Control

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"lane":str?,"time":ticks?}
```

## mixer.recordStart

Start Automation Pass

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.recordStart`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## mixer.recordStop

Write Automation

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.recordStop`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## clipMixer.set

Audio Clip Mixer Adjust

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipMixer.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":"volume"|"panner","param":"level"|"balance","value":f64,"keyframe":bool?,"time":ticks?,"begin":bool?}
```

## clipMixer.setMode

Audio Clip Mixer Automation Mode

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipMixer.setMode`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"A1"|id,"mode":"Off|Read|Latch|Touch|Write"}
```

## clipMixer.touch

Touch Clip Mixer Control

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipMixer.touch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"A1"|id,"lane":"volume|pan","value":f64,"time":ticks?}
```

## clipMixer.release

Release Clip Mixer Control

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clipMixer.release`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"A1"|id,"lane":"volume|pan","time":ticks?}
```

## effects.setDefaultTransition

Set Selected as Default Transition

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe effects.setDefaultTransition`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"effect":"constant_power|constant_gain|exponential_fade|<video transition>"}
```

## mixer.deleteSubmix

Delete Submix Track

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.deleteSubmix`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"S1"|id}
```

## mixer.addInsert

Add Track Effect

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.addInsert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"effect":str,"slot":n?,"postFader":bool?}
```

## mixer.removeInsert

Remove Track Effect

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.removeInsert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"slot":n}
```

## mixer.setInsert

Track Effect Settings

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.setInsert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"slot":n,"enabled":bool?,"postFader":bool?,"params":{id:value}?}
```

## mixer.addSend

Add Send

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.addSend`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|id,"target":"S1"|id,"levelDb":f64?,"preFader":bool?,"pan":f64?}
```

## mixer.setSend

Send Settings

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.setSend`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|id,"send":n,"levelDb":f64?,"pan":f64?,"preFader":bool?,"muted":bool?,"target":"S1"?}
```

## mixer.removeSend

Remove Send

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.removeSend`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|id,"send":n}
```

## mixer.setKeyframe

Add Track Keyframe

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.setKeyframe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"lane":str?,"time":ticks?,"value":f64}
```

## mixer.deleteKeyframe

Delete Track Keyframe

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.deleteKeyframe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"lane":str?,"time":ticks}
```

## mixer.moveKeyframe

Move Track Keyframe

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.moveKeyframe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"lane":str?,"time":ticks,"newTime":ticks?,"value":f64?}
```

## mixer.clearLane

Clear Track Keyframes

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.clearLane`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"lane":str?}
```

## mixer.writeAutomation

Write Automation Points

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mixer.writeAutomation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strip":"A1"|"S1"|"Mix"|id,"lane":str?,"points":[[ticks,value]],"tolerance":f64?}
```

## clip.synchronize

Synchronize…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.synchronize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"method":"in|out|timecode|marker|audio","clips":[id]?,"reference":clip?,"track":"V1"|"A1"?,"ignoreHours":bool?,"marker":str?,"offset":frames?}
```

## clip.mergeClips

Merge Clips…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.mergeClips`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"method":"in|out|timecode|marker|audio","name":str?,"removeVideoAudio":bool?,"ignoreHours":bool?,"marker":str?,"offset":frames?}
```

## clip.createMulticam

Create Multi-Camera Source Sequence…

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.createMulticam`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"name":str?,"method":"in|out|timecode|marker|audio","ignoreHours":bool?,"marker":str?,"offset":frames?,"audio":"camera1|all|switch","cameraNames":"clip|track|metadata","processedBin":bool?,"reference":item?}
```

## clip.multicamEnable

Enable

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.multicamEnable`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"enabled":bool?}
```

## clip.multicamFlatten

Flatten

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.multicamFlatten`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## multicam.switchAngle

Switch Multi-Camera Angle

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.switchAngle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"camera":1..16 (shown order)|"angle":0-based,"clips":[id]?,"time":ticks?,"videoOnly":bool?,"audioOnly":bool?}
```

## multicam.recordStart

Start Multi-Camera Recording

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.recordStart`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## multicam.cut

Cut to Camera

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"camera":1..16|"angle":0-based,"time":ticks?,"videoOnly":bool?}
```

## multicam.recordStop

Stop Multi-Camera Recording

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.recordStop`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## multicam.audioFollowsVideo

Multi-Camera Audio Follows Video

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.audioFollowsVideo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"enabled":bool?}
```

## multicam.editCameras

Edit Cameras…

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.editCameras`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"sequence":id?,"cameras":[{"angle":0-based,"name":str?,"enabled":bool?}]?,"audio":"camera1|all|switch"?}
```

## multicam.cutToCamera

Cut to Camera

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"camera":1..16|"angle":0-based,"time":ticks?,"videoOnly":bool?}
```

## multicam.gridLayout

Multi-Camera Layout

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.gridLayout`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layout":"auto|2x2|3x3|4x4"}
```

## multicam.page

Multi-Camera Page

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.page`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"page":0-based|"next"|"prev"}
```

## multicam.nextPage

Next Multi-Camera Page

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.nextPage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## multicam.prevPage

Previous Multi-Camera Page

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.prevPage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## multicam.selectionTopDown

Multi-Camera Selection Top Down

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectionTopDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"enabled":bool?}
```

## multicam.showPreviewMonitor

Show Multi-Camera Preview Monitor

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.showPreviewMonitor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"enabled":bool?}
```

## multicam.autoAdjustQuality

Auto-Adjust Multi-Camera Playback Quality

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.autoAdjustQuality`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"enabled":bool?}
```

## multicam.transmitView

Transmit Multi-Camera View

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.transmitView`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"enabled":bool?}
```

## multicam.grid

Multi-Camera Grid

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.grid`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"playing":bool?,"cellPixels":f32?,"playbackScale":f32?}
```

## multicam.inspect

Inspect Multi-Camera

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## multicam.selectCamera1

Select Camera 1

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera1`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera1

Cut to Camera 1

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera1`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.selectCamera2

Select Camera 2

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera2`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera2

Cut to Camera 2

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera2`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.selectCamera3

Select Camera 3

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera3`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera3

Cut to Camera 3

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera3`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.selectCamera4

Select Camera 4

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera4`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera4

Cut to Camera 4

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera4`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.selectCamera5

Select Camera 5

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera5

Cut to Camera 5

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.selectCamera6

Select Camera 6

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera6`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera6

Cut to Camera 6

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera6`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.selectCamera7

Select Camera 7

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera7`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera7

Cut to Camera 7

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera7`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.selectCamera8

Select Camera 8

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera8`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera8

Cut to Camera 8

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera8`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.selectCamera9

Select Camera 9

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.selectCamera9`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## multicam.cutToCamera9

Cut to Camera 9

- 技能 / Owner: `filmcraft-cli-multicam`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-multicam`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe multicam.cutToCamera9`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"videoOnly":bool?}
```

## essentialSound.inspect

Inspect Essential Sound

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## essentialSound.setType

Set Audio Type

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.setType`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"type":"dialogue|music|sfx|ambience"}
```

## essentialSound.clearType

Clear Audio Type

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.clearType`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## essentialSound.set

Essential Sound Setting

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"key":"repair.noise.on|repair.noise.amount|repair.humHz|clarity.eqPreset|creative.reverbPreset|ducking.reduceDb|volume.levelDb|mute|…","value":any,"values":{key:value}?,"begin":bool?}
```

## essentialSound.applyPreset

Apply Sound Preset

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.applyPreset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"preset":str,"type":"dialogue|music|sfx|ambience"?}
```

## essentialSound.savePreset

Save Sound Preset

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.savePreset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"name":str}
```

## essentialSound.deletePreset

Delete Sound Preset

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.deletePreset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"type":"dialogue|music|sfx|ambience"?}
```

## essentialSound.autoMatch

Auto-Match Loudness

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.autoMatch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"target":lufs?}
```

## essentialSound.generateDucking

Generate Ducking Keyframes

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe essentialSound.generateDucking`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?}
```

## color.spaces

List Colour Spaces

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe color.spaces`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## lumetri.presets

List Lumetri Presets

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lumetri.presets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"folder":str?}
```

## lumetri.applyPreset

Apply Lumetri Preset

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lumetri.applyPreset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"clips":[id]?}
```

## lumetri.presetThumbnails

Lumetri Preset Thumbnails

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lumetri.presetThumbnails`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"folder":str?,"names":[str]?,"width":n=160,"columns":n=4,"path":str?}
```

## media.colorInfo

Media Colour Info

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.colorInfo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id}
```

## lut.import

Import LUT…

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lut.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"name":str?}
```

## lut.list

List LUTs

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lut.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## lut.remove

Remove LUT

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lut.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":str}
```

## lut.export

Export LUT

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lut.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"lut":"lib:<id>"|"builtin:<id>","path":str,"format":"cube"|"3dl"?}
```

## lumetri.setInputLut

Set Input LUT

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lumetri.setInputLut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"lut":"lib:<id>"|"builtin:<id>"|""?,"path":str?}
```

## lumetri.setLook

Set Creative Look

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lumetri.setLook`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"lut":"lib:<id>"|"builtin:<id>"|""?,"path":str?}
```

## lumetri.applyMatch

Apply Match

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lumetri.applyMatch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"referenceTime":ticks?|"referenceFrame":n?|"referenceTimecode":str?,"faceDetection":bool=true}
```

## lumetri.setSection

Toggle Lumetri Section

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe lumetri.setSection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"section":"basic"|"creative"|"curves"|"wheels"|"hsl"|"vignette","on":bool?}
```

## graphics.newText

Text

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.newText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"text":str="New Text","position":[x,y]?,"clip":id?,"newClip":bool?,"vertical":bool=false,"size":px=100,"font":str?,"fontStyle":str?,"seconds":f64=5,"track":index?,"time":ticks?}
```

## graphics.newShape

Shape

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.newShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"shape":"rectangle|ellipse|polygon|path","position":[x,y]?,"size":[w,h]=[400,200],"points":[[x,y],…]?,"clip":id?,"seconds":f64=5}
```

## graphics.setText

Edit Text

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.setText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n|name?,"text":str,"merge":bool? (coalesce with the previous Edit Text undo step)}
```

## graphics.set

Set Graphic Properties

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n|name?,"props":{"font":"Inter","font_style":"Bold","size":120,"align":"center","tracking":50,"leading":0,"fill_color":"#ffcc00","stroke":true,"stroke_width":6,"background":true,"shadow":true,"position":[x,y],"scale":100,"rotation":0,"opacity":100,…},"time":ticks?}
```

## graphics.selectLayer

Select Graphic Layer

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.selectLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]}
```

## graphics.deleteLayer

Delete Graphic Layer

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.deleteLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n?}
```

## graphics.arrangeLayer

Arrange Graphic Layer

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.arrangeLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n?,"to":"front|back|forward|backward"|index}
```

## graphics.align

Align Layers

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.align`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]?,"align":"left|hcenter|right|top|vcenter|bottom","to":"frame|group|selection"="frame" (frame: each layer; group: the layers' union; one layer always aligns to the frame)}
```

## graphics.distribute

Distribute Layers

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.distribute`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n] (3 or more)?,"axis":"horizontal|vertical","space":bool=false (equal gaps instead of equal centre spacing)}
```

## graphics.list

List Graphic Layers

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?}
```

## fonts.list

List Fonts

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe fonts.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"system":bool=true (scan the system font folders)}
```

## graphics.newVerticalText

Vertical Text

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.newVerticalText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"text":str="New Text","position":[x,y]?,"clip":id?,"size":px=100,"seconds":f64=5,"time":ticks?}
```

## graphics.newRectangle

Rectangle

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.newRectangle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"position":[x,y]?,"size":[w,h]=[400,200],"clip":id?}
```

## graphics.newEllipse

Ellipse

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.newEllipse`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"position":[x,y]?,"size":[w,h]=[400,200],"clip":id?}
```

## graphics.newPolygon

Polygon

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.newPolygon`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"position":[x,y]?,"size":[w,h]=[300,300],"sides":n=6,"clip":id?}
```

## graphics.newFromFile

From file…

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.newFromFile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"time":ticks?,"track":index?} (imports the image or video and places it above the clips at the playhead)
```

## graphics.alignFrame.left

Left

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignFrame.left`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignFrame.hcenter

Center Horizontally

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignFrame.hcenter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignFrame.right

Right

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignFrame.right`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignFrame.top

Top

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignFrame.top`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignFrame.vcenter

Center Vertically

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignFrame.vcenter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignFrame.bottom

Bottom

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignFrame.bottom`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignGroup.left

Left

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignGroup.left`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignGroup.hcenter

Center Horizontally

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignGroup.hcenter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignGroup.right

Right

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignGroup.right`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignGroup.top

Top

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignGroup.top`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignGroup.vcenter

Center Vertically

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignGroup.vcenter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignGroup.bottom

Bottom

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignGroup.bottom`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignSelection.left

Left

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignSelection.left`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignSelection.hcenter

Center Horizontally

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignSelection.hcenter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignSelection.right

Right

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignSelection.right`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignSelection.top

Top

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignSelection.top`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignSelection.vcenter

Center Vertically

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignSelection.vcenter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.alignSelection.bottom

Bottom

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignSelection.bottom`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.distributeVertically

Distribute Vertically

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.distributeVertically`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.distributeSpaceVertically

Distribute Space Vertically

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.distributeSpaceVertically`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.distributeHorizontally

Distribute Horizontally

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.distributeHorizontally`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.distributeSpaceHorizontally

Distribute Space Horizontally

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.distributeSpaceHorizontally`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers)}
```

## graphics.bringToFront

Bring to Front

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.bringToFront`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n?}
```

## graphics.bringForward

Bring Forward

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.bringForward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n?}
```

## graphics.sendBackward

Send Backward

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.sendBackward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n?}
```

## graphics.sendToBack

Send to Back

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.sendToBack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n?}
```

## graphics.selectNextGraphic

Select Next Graphic

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.selectNextGraphic`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.selectPreviousGraphic

Select Previous Graphic

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.selectPreviousGraphic`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.selectNextLayer

Select Next Layer

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.selectNextLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.selectPreviousLayer

Select Previous Layer

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.selectPreviousLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.resetAllParameters

Reset All Parameters

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.resetAllParameters`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layers":[n]? (default: the selected layers, else all)}
```

## graphics.resetDuration

Reset Duration

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.resetDuration`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"seconds":f64=5 (the default graphic duration; limited by the next clip on the track)}
```

## graphics.template.list

List Graphics Templates

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.template.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"query":str? (search names, categories, descriptions, tags),"category":str?,"source":"builtin|user"?}
```

## graphics.template.apply

Apply Graphics Template

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.template.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"template":id|name|path,"values":{control id or name: value}?,"time":ticks?,"track":index?}
```

## graphics.template.export

Export As Motion Graphics Template…

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.template.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"name":str,"category":str="My Templates","description":str?,"controls":[{"layer":n|name,"param":"text|fill_color|size|font|position|enabled|…","name":str?,"kind":"text|color|slider|checkbox|font|position"?,"min":f64?,"max":f64?,"id":str?}]? (default: each text layer's text),"path":str? (default: the user templates folder),"embedFonts":bool=false,"fontLicense":str?}
```

## file.exportGraphicsTemplate

Motion Graphics Template…

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportGraphicsTemplate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
as graphics.template.export
```

## graphics.template.install

Install Motion Graphics Template…

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.template.install`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str (a .fcgt file; Adobe .mogrt files are refused)}
```

## graphics.template.remove

Remove Graphics Template

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.template.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"template":id|name (a user template)}
```

## graphics.template.set

Set Template Property

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.template.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"control":id|name,"value":any} or {"clip":id?,"values":{control: value}}
```

## graphics.template.controls

List Template Properties

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.template.controls`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?}
```

## graphics.template.thumbnail

Graphics Template Thumbnail

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.template.thumbnail`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"template":id|name|path,"width":px=320,"path":str? (write a PNG there; else returned as pngBase64)}
```

## graphics.setRoll

Roll/Crawl Options

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.setRoll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"mode":"off|roll|crawlLeft|crawlRight"?,"startOffScreen":bool?,"endOffScreen":bool?,"prerollFrames":n?,"easeInFrames":n?,"easeOutFrames":n?,"postrollFrames":n? (or …Seconds, or ticks as preroll/easeIn/easeOut/postroll)}
```

## graphics.setResponsiveTime

Responsive Design - Time

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.setResponsiveTime`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"introFrames":n?,"outroFrames":n? (or introSeconds / outroSeconds, or ticks as intro / outro)}
```

## graphics.pin

Responsive Design - Position

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.pin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n|name?,"to":"frame"|"none"|layer index|layer name,"edges":["left","top","right","bottom"]|"all"="all"}
```

## graphics.setCharStyle

Character Style

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.setCharStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"layer":n|name?,"start":char=0,"end":char=len,"style":{"font":str,"fontStyle":str,"size":px,"color":"#rrggbb","bold":bool,"italic":bool,"underline":bool,"tracking":n,"baselineShift":px,"caps":"normal|all caps|small caps"},"clear":bool? (remove styles from the range)}
```

## graphics.upgradeCaption

Upgrade Caption to Graphic

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.upgradeCaption`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"captions":[id]? (default: the selected captions, else the one under the playhead)}
```

## graphics.upgradeToSourceGraphic

Upgrade to Source Graphic

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.upgradeToSourceGraphic`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?}
```

## file.replaceFonts

Replace Fonts in Projects…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.replaceFonts`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":family|{"family","style"?},"to":family|{"family","style"?},"toStyle":str?}
```

## graphics.fonts.used

List Fonts Used

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.fonts.used`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## shortcuts.list

List Keyboard Shortcuts

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"query":str?,"panel":str?,"assigned":bool?,"platform":"mac|windows|linux"?}
```

## shortcuts.get

Get Shortcuts of a Command

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"command":id,"platform":str?}
```

## shortcuts.set

Assign Shortcut

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"command":id,"keys":"Cmd+Shift+K","panel":str?,"add":bool?,"keepConflicts":bool?}
```

## shortcuts.clear

Clear Shortcut

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"command":id,"keys":str?,"panel":str?}
```

## shortcuts.undo

Undo Shortcut Change

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.undo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## shortcuts.redo

Redo Shortcut Change

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.redo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## shortcuts.conflicts

Shortcut Conflicts

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.conflicts`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"platform":"mac|windows|linux"?}
```

## shortcuts.forKey

Shortcuts on a Key

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.forKey`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"key":"K","platform":str?}
```

## shortcuts.resolve

Resolve Shortcut

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.resolve`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"keys":str,"panel":str?,"platform":str?}
```

## shortcuts.presets

Keyboard Shortcut Presets

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.presets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## shortcuts.loadPreset

Load Shortcut Preset

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.loadPreset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str}
```

## shortcuts.savePreset

Save Shortcut Preset As

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.savePreset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str}
```

## shortcuts.deletePreset

Delete Shortcut Preset

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.deletePreset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str}
```

## shortcuts.export

Export Keyboard Shortcuts

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## shortcuts.import

Import Keyboard Shortcuts

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"activate":bool=true}
```

## shortcuts.audit

Shortcut Audit

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shortcuts.audit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## media.findMissing

Find Missing Media

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.findMissing`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## media.status

Media Status

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.status`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?}
```

## media.linkMedia

Link Media…

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.linkMedia`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}  (opens the Link Media dialog; agents use media.relink / media.autoRelink)
```

## media.relink

Relink Media

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.relink`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id,"path":str,"force":bool=false,"relinkOthers":bool=true,"alignTimecode":bool=false,"match":{"fileName":bool,"extension":bool,"clipId":bool,"duration":bool,"mediaStart":bool,"metadata":bool}?}
```

## media.replaceFootage

Replace Footage…

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.replaceFootage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id,"path":str}
```

## media.autoRelink

Relink Moved Media

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.autoRelink`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":str,"to":str}|{"folder":str} + match options
```

## media.search

Search for Media

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.search`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"folder":str,"item":id?,"exactName":bool=true}
```

## media.makeOffline

Make Offline…

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.makeOffline`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"deleteFiles":bool=false}
```

## file.importFromMediaBrowser

Import from Media Browser

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.importFromMediaBrowser`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"paths":[str]?,"imageSequence":bool?}
```

## file.import

Import…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"paths":[str],"bin":binId?,"imageSequence":bool?}
```

## file.importImageSequence

Import Image Sequence…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.importImageSequence`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"bin":binId?,"frameRate":{"num":i64,"den":i64}?}
```

## media.offlineAll

Offline All

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.offlineAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}  (leave every missing file offline and close the Link Media dialog)
```

## media.createProxies

Create Proxies…

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.createProxies`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"preset":"prores_proxy_quarter|prores_proxy_half|prores_lt_half|h264_quarter|h264_half","destination":str?,"attach":bool=true,"wait":bool=false}
```

## media.attachProxies

Attach Proxies…

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.attachProxies`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id,"path":str}|{"items":[id],"paths":[str]},"force":bool=false
```

## media.detachProxies

Detach Proxies

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.detachProxies`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## media.reconnectFullRes

Reconnect Full Resolution Media…

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.reconnectFullRes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id,"path":str}
```

## media.toggleProxies

Toggle Proxies

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.toggleProxies`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"enabled":bool?}
```

## media.proxyPresets

Proxy Presets

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe media.proxyPresets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.mediaPropertiesFile

File…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.mediaPropertiesFile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## file.mediaProperties

Selection…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.mediaProperties`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## file.projectSettings.general

General…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.projectSettings.general`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"renderer":"gpu|software"?,"videoDisplay":"timecode|feet35|feet16|frames"?,"audioDisplay":"samples|milliseconds"?,"captureFormat":"DV|HDV"?,"titleSafe":[h,v]?,"actionSafe":[h,v]?}
```

## file.projectSettings.scratchDisks

Scratch Disks…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.projectSettings.scratchDisks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"captured":path|null?,"videoPreviews":path|null?,"audioPreviews":path|null?,"autoSave":path|null?}
```

## project.ingestSettings

Ingest Settings…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.ingestSettings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"enabled":bool?,"action":"copy|transcode|createProxies|copyAndCreateProxies"?,"destination":str?,"preset":str?}
```

## file.projectManager

Project Manager…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.projectManager`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"destination":str,"mode":"collect|consolidate","sequences":[id]?,"excludeUnused":bool=true,"handles":frames=30,"preset":"prores_lt|prores_hq|h264|…","includeProxies":bool,"includePreviews":bool=false,"projectName":str?,"dryRun":bool=false,"overwrite":bool=false,"wait":bool=false}
```

## masks.add

Create Mask

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?="opacity","shape":"ellipse"|"polygon"|"bezier","path":[[x,y]…]|{vertices}?,"center":[x,y]?,"size":[w,h]?}
```

## masks.remove

Delete Mask

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?,"mask":n?}
```

## masks.set

Change Mask

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?,"mask":n?,"name":str?,"inverted":bool?,"mode":"none|add|subtract|intersect|lighten|darken|difference"?,"trackMethod":"position|positionRotation|positionScaleRotation"?,"feather":px?,"opacity":pct?,"expansion":px?,"path":path?,"time":ticks?,"merge":key?}
```

## masks.moveVertex

Move Mask Vertex

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.moveVertex`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?,"mask":n?,"vertex":n,"handle":"point"|"in"|"out"?,"to":[x,y]?|"delta":[dx,dy]?,"breakHandles":bool?,"merge":key?}
```

## masks.translate

Move Mask

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.translate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?,"mask":n?,"delta":[dx,dy],"merge":key?}
```

## masks.addVertex

Add Mask Vertex

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.addVertex`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?,"mask":n?,"after":n,"at":[x,y]}
```

## masks.removeVertex

Delete Mask Vertex

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.removeVertex`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?,"mask":n?,"vertex":n}
```

## masks.track

Track Selected Mask

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.track`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?,"mask":n?,"direction":"forward"|"backward"?,"frames":n?,"method":"position|positionRotation|positionScaleRotation"?,"wait":bool?}
```

## masks.toggleVertexSmooth

Convert Mask Vertex

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.toggleVertexSmooth`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effect":index|id?,"mask":n?,"vertex":n}
```

## masks.select

Select Mask

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id,"effect":index|id,"mask":n}|{"none":true}
```

## masks.list

List Masks

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe masks.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"time":ticks?}
```

## presets.list

List Effect Presets

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## presets.save

Save Preset

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe presets.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"effects":[index]?,"name":str,"description":str?,"keyframes":"scale"|"anchorIn"|"anchorOut"|"none"?}
```

## presets.apply

Apply Preset

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe presets.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":str,"clips":[id]?}
```

## presets.delete

Delete Preset

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe presets.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str}
```

## presets.rename

Rename Preset

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe presets.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"to":str}
```

## presets.export

Export Presets

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe presets.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"names":[str]?}
```

## presets.import

Import Presets

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe presets.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## export.presets.list

List Export Presets

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"query":str?,"category":str?,"format":str?,"favorites":bool?}
```

## export.presets.get

Get Export Preset

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.presets.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str}
```

## export.presets.save

Save Export Preset

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.presets.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"from":str?,"settings":ExportSettings?,"category":str?,"description":str?,"overwrite":bool=true, …flat overrides}
```

## export.presets.delete

Delete Export Preset

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.presets.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str}
```

## export.presets.favorite

Favorite Export Preset

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.presets.favorite`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"favorite":bool?}
```

## export.presets.import

Import Export Presets

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.presets.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## export.presets.export

Export Export Presets

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.presets.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"names":[str]?}
```

## export.formats

List Export Formats

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.formats`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## export.resolve

Resolve Export Settings

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.resolve`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{…settings params, "path":str?}
```

## export.queue.add

Send to Export Queue

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{…settings params,"path":str|dir?,"sequences":[id]?,"ranges":[range]?,"start":bool?,"wait":bool?}
```

## export.queue.list

List Export Queue

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## export.queue.start

Start Export Queue

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.start`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"wait":bool=false}
```

## export.queue.stop

Stop Export Queue

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.stop`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## export.queue.cancel

Cancel Queued Export

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.cancel`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":id?,"wait":bool?}
```

## export.queue.retry

Retry Queued Export

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.retry`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":id,"start":bool?,"wait":bool?}
```

## export.queue.remove

Remove Queued Export

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":id}
```

## export.queue.move

Reorder Queued Export

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":id,"to":index?,"by":int?}
```

## export.queue.clear

Clear Finished Exports

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.queue.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"all":bool=false}
```

## export.quick

Quick Export

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe export.quick`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":str?,"path":str?,"wait":bool?, …settings params}
```

## transcript.generate

Transcribe…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.generate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"model":"whisper-base"?,"language":"en|auto"?,"diarize":bool?,"maxSpeakers":n?}
```

## transcript.set

Import Transcript

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id,"transcript":{"language":str,"speakers":[{"name":str}],"words":[{"text":str,"start":tick,"end":tick,"speaker":n?}]}}
```

## transcript.delete

Delete Transcript

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## transcript.inspect

Inspect Transcript

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"paragraphGapSeconds":f?}
```

## transcript.search

Search Transcript

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.search`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"query":str}
```

## transcript.models

List Speech Models

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.models`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## transcript.downloadModel

Download Speech Model

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.downloadModel`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"model":"whisper-base"?}
```

## transcript.select

Mark Selected Text

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":word,"to":word?}
```

## transcript.extract

Extract Selected Text

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.extract`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":word,"to":word?}
```

## transcript.lift

Lift Selected Text

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.lift`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":word,"to":word?}
```

## transcript.renameSpeaker

Rename Speaker…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.renameSpeaker`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"speaker":"Speaker 1"|index,"name":str,"item":id?}
```

## transcript.removePauses

Remove Pauses

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.removePauses`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"minSeconds":f?,"keepSeconds":f?}
```

## transcript.removeFillers

Remove Filler Words

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.removeFillers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"fillers":[str]?}
```

## transcript.createCaptions

Create Captions from Transcript…

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe transcript.createCaptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"maxChars":n?,"lines":1|2?,"minSeconds":f?,"maxSeconds":f?,"gapFrames":n?,"format":str?,"name":str?}
```

## events.list

List Events

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe events.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"level":"info|warning|error"?,"since":id?}
```

## events.clear

Clear All Events

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe events.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## metadata.get

Get Metadata

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe metadata.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?,"clip":id?}
```

## metadata.set

Edit Metadata

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe metadata.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?,"clip":id?,"field":"Name|Label|Description|Scene|Shot|Log Note|Comment|Tape Name|Client|Camera Angle|…","value":str} | {"item":id?,"fields":{name:str}}
```

## scopes.read

Read Lumetri Scopes

- 技能 / Owner: `filmcraft-cli-color`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-color`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe scopes.read`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"scopes":["waveform","parade","histogram","vectorscopeYuv","vectorscopeHls"]?,"waveformType":"rgb|luma|yc|ycNoChroma"?,"paradeType":"rgb|yuv|rgbWhite"?,"colorSpace":"auto|601|709|2100"?,"clamp":bool=true,"columns":n=8,"peaks":n=8,"bins":bool=true,"scale":0.5,"time":ticks?|"frame"|"seconds"|"timecode"}
```

## clip.remix.enable

Enable Remix

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.remix.enable`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?}
```

## clip.remix.properties

Remix Properties…

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.remix.properties`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"duration":ticks?,"seconds":f64?,"frame":n?,"timecode":str?,"segments":0..100?,"variations":0..100?}
```

## clip.remix.revert

Revert Remix

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.remix.revert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?}
```

## clip.remix

Remix

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.remix`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clip":id?,"duration":ticks?,"seconds":f64?,"frame":n?,"timecode":str?,"segments":0..100?,"variations":0..100?}
```

## audio.voiceover.settings

Voice-Over Record Settings

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe audio.voiceover.settings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"source":str?,"inputChannel":n?,"name":str?,"countdownSoundCues":bool?,"prerollSeconds":f64?,"postrollSeconds":f64?}
```

## audio.voiceover.start

Start Voice-over Recording

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe audio.voiceover.start`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"track":"A1"|id?,"time":ticks?,"preroll":seconds?}
```

## audio.voiceover.sync

Sync Voice-over Capture

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe audio.voiceover.sync`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?}
```

## audio.voiceover.stop

Stop Voice-over Recording

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe audio.voiceover.stop`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"time":ticks?,"dir":str?,"discard":bool?}
```

## playhead.nextEditAnyTrack

Go to Next Edit Point on Any Track

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.nextEditAnyTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.prevEditAnyTrack

Go to Previous Edit Point on Any Track

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.prevEditAnyTrack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.selectedClipStart

Go to Selected Clip Start

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.selectedClipStart`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## playhead.selectedClipEnd

Go to Selected Clip End

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe playhead.selectedClipEnd`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## sequence.revealNested

Reveal Nested Sequence

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe sequence.revealNested`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.selectClipAtPlayhead

Select Clip at Playhead

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.selectClipAtPlayhead`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.selectNextClip

Select Next Clip

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.selectNextClip`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.selectPrevClip

Select Previous Clip

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.selectPrevClip`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.extendPreviousEdit

Extend Previous Edit To Playhead

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.extendPreviousEdit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## trim.extendNextEdit

Extend Next Edit To Playhead

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe trim.extendNextEdit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.nudgeLeft

Nudge Clip Selection Left One Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.nudgeLeft`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.nudgeRight

Nudge Clip Selection Right One Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.nudgeRight`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.nudgeLeft5

Nudge Clip Selection Left Five Frames

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.nudgeLeft5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.nudgeRight5

Nudge Clip Selection Right Five Frames

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.nudgeRight5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.nudgeUp

Nudge Clip Selection Up

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.nudgeUp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.nudgeDown

Nudge Clip Selection Down

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.nudgeDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.slipLeft

Slip Clip Selection Left One Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slipLeft`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.slipRight

Slip Clip Selection Right One Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slipRight`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.slipLeft5

Slip Clip Selection Left Five Frames

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slipLeft5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.slipRight5

Slip Clip Selection Right Five Frames

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slipRight5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.slideLeft

Slide Clip Selection Left One Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slideLeft`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.slideRight

Slide Clip Selection Right One Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slideRight`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.slideLeft5

Slide Clip Selection Left Five Frames

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slideLeft5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.slideRight5

Slide Clip Selection Right Five Frames

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.slideRight5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleAllVideoTargets

Toggle All Video Targets

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleAllVideoTargets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleAllAudioTargets

Toggle All Audio Targets

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleAllAudioTargets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleAllSourceVideo

Toggle All Source Video

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleAllSourceVideo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleAllSourceAudio

Toggle All Source Audio

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleAllSourceAudio`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.moveVideoTargetsUp

Move All Video Targets Up

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.moveVideoTargetsUp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.moveVideoTargetsDown

Move All Video Targets Down

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.moveVideoTargetsDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.moveAudioTargetsUp

Move All Audio Targets Up

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.moveAudioTargetsUp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.moveAudioTargetsDown

Move All Audio Targets Down

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.moveAudioTargetsDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleMuteTargetedAudio

Toggle Mute for All Targeted Audio Tracks

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleMuteTargetedAudio`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleSoloTargetedAudio

Toggle Solo for All Targeted Audio Tracks

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleSoloTargetedAudio`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleOutputTargetedVideo

Toggle Track Output for All Targeted Video Tracks

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleOutputTargetedVideo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.volumeUp

Increase Clip Volume

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.volumeUp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.volumeDown

Decrease Clip Volume

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.volumeDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.volumeUpMany

Increase Clip Volume Many

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.volumeUpMany`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.volumeDownMany

Decrease Clip Volume Many

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.volumeDownMany`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.nudgeVolumeUp1

Nudge Volume +1dB

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.nudgeVolumeUp1`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.nudgeVolumeUp3

Nudge Volume +3dB

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.nudgeVolumeUp3`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.nudgeVolumeDown1

Nudge Volume -1dB

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.nudgeVolumeDown1`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## clip.nudgeVolumeDown3

Nudge Volume -3dB

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.nudgeVolumeDown3`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## audio.toggleScrubbing

Toggle Audio During Scrubbing

- 技能 / Owner: `filmcraft-cli-audio`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-audio`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe audio.toggleScrubbing`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.fontSizeUp

Increase Font Size by One Unit

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.fontSizeUp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.fontSizeDown

Decrease Font Size by One Unit

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.fontSizeDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.fontSizeUp5

Increase Font Size by Five Units

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.fontSizeUp5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.fontSizeDown5

Decrease Font Size by Five Units

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.fontSizeDown5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.leadingUp

Increase Leading by One Unit

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.leadingUp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.leadingDown

Decrease Leading by One Unit

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.leadingDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.leadingUp5

Increase Leading by Five Units

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.leadingUp5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.leadingDown5

Decrease Leading by Five Units

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.leadingDown5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.alignTextLeft

Left align text

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignTextLeft`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.alignTextCenter

Center align text

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignTextCenter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.alignTextRight

Right align text

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.alignTextRight`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.nudgeLeft

Nudge Selected Object to left by one

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.nudgeLeft`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.nudgeRight

Nudge Selected Object to right by one

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.nudgeRight`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.nudgeUp

Nudge Selected Object up by one

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.nudgeUp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.nudgeDown

Nudge Selected Object down by one

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.nudgeDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.nudgeLeft5

Nudge Selected Object to left by five

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.nudgeLeft5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.nudgeRight5

Nudge Selected Object to right by five

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.nudgeRight5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.nudgeUp5

Nudge Selected Object up by five

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.nudgeUp5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## graphics.nudgeDown5

Nudge Selected Object down by five

- 技能 / Owner: `filmcraft-cli-motion`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-motion`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe graphics.nudgeDown5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.exportFrame

Export Frame

- 技能 / Owner: `filmcraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.exportFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str?,"format":"png|tiff|bmp"?,"import":bool?}
```

## clip.setPosterFrame

Set Poster Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.setPosterFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?,"time":ticks?}
```

## clip.clearPosterFrame

Clear Poster Frame

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.clearPosterFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"item":id?}
```

## timeline.toggleTargetV1

Toggle Target Video 1

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetV1`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetV2

Toggle Target Video 2

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetV2`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetV3

Toggle Target Video 3

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetV3`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetV4

Toggle Target Video 4

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetV4`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetV5

Toggle Target Video 5

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetV5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetV6

Toggle Target Video 6

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetV6`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetV7

Toggle Target Video 7

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetV7`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetV8

Toggle Target Video 8

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetV8`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetA1

Toggle Target Audio 1

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetA1`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetA2

Toggle Target Audio 2

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetA2`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetA3

Toggle Target Audio 3

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetA3`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetA4

Toggle Target Audio 4

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetA4`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetA5

Toggle Target Audio 5

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetA5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetA6

Toggle Target Audio 6

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetA6`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetA7

Toggle Target Audio 7

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetA7`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## timeline.toggleTargetA8

Toggle Target Audio 8

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.toggleTargetA8`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## project.view.get

Project Panel View

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.view.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## project.view.set

Set Project Panel View

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.view.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"view":"list|icon|freeform"?,"iconSize":f32?,"fontSize":"small|medium|large|extraLarge"?,"previewArea":bool?,"thumbnails":bool?,"thumbnailsShowEffects":bool?,"hoverScrub":bool?,"thumbnailControlsAllDevices":bool?,"iconSort":column|{"column":str,"descending":bool}?}
```

## project.columns.list

List Project Columns

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.columns.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## project.columns.set

Metadata Display

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.columns.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"columns":[name|{"name":str,"width":f32}]}
```

## project.columns.resize

Resize Column

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.columns.resize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"column":str,"width":f32}
```

## project.sort

Sort Project Items

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.sort`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"column":str,"descending":bool?}
```

## project.items

List Project Panel Rows

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.items`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":binId?,"recursive":bool?}
```

## project.viewPreset.list

List View Presets

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.viewPreset.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## project.viewPreset.save

Save Current View Preset

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.viewPreset.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"slot":1..10?,"name":str?}
```

## project.viewPreset.saveAs

Save As New View Preset

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.viewPreset.saveAs`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"slot":1..10?}
```

## project.viewPreset.restore

Restore View Preset

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.viewPreset.restore`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"slot":1..10}
```

## project.viewPreset.rename

Rename View Preset

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.viewPreset.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"slot":1..10,"name":str}
```

## project.viewPreset.delete

Delete View Preset

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.viewPreset.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"slot":1..10}
```

## project.freeform.layout

Freeform Layout

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.layout`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":binId?,"width":f32?}
```

## project.freeform.move

Move Clip Cards

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"x":f32,"y":f32,"snap":bool?} | {"positions":{"<id>":[x,y]}}
```

## project.freeform.resize

Clip Size

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.resize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?,"size":f32?,"step":1|-1?}
```

## project.freeform.alignToGrid

Align to Grid

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.alignToGrid`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":binId?,"grid":f32?}
```

## project.freeform.reset

Reset to Grid

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":binId?}
```

## project.freeform.stack

Stack Clips

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.stack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## project.freeform.unstack

Unstack Clips

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.unstack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"items":[id]?}
```

## project.freeform.saveArrangement

Save Arrangement

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.saveArrangement`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"bin":binId?}
```

## project.freeform.restoreArrangement

Restore Arrangement

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.restoreArrangement`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"bin":binId?}
```

## project.freeform.deleteArrangement

Delete Arrangement

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.deleteArrangement`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"bin":binId?}
```

## project.freeform.arrangements

List Arrangements

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.arrangements`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":binId?}
```

## project.freeform.options

Freeform View Options…

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.freeform.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"grid":f32?,"snap":bool?,"showNames":bool?,"showDurations":bool?,"cardSize":f32?}
```

## project.renameBin

Rename Bin

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.renameBin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":binId,"name":str}
```

## mediaBrowser.roots

Media Browser Locations

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.roots`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## mediaBrowser.list

List Directory

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str?,"fileTypes":str?}
```

## mediaBrowser.navigate

Go to Directory

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.navigate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str} | {"back":true} | {"forward":true} | {"up":true}
```

## mediaBrowser.select

Select Files

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"paths":[str]}
```

## mediaBrowser.favorite

Add to Favorites

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.favorite`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str?,"remove":bool?}
```

## mediaBrowser.clearRecent

Clear Recent Directories

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.clearRecent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## mediaBrowser.settings

Media Browser Settings

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.settings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"fileTypes":"all|video|audio|image|project|caption|<ext>"?,"view":"list|thumbnails"?,"columns":[str]?,"importAsImageSequence":bool?,"hoverScrub":bool?,"thumbnailSize":f32?}
```

## mediaBrowser.import

Import

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"paths":[str]?,"bin":binId?,"imageSequence":bool?}
```

## mediaBrowser.openInSource

Open In Source Monitor

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.openInSource`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str?}
```

## mediaBrowser.probe

Media File Properties

- 技能 / Owner: `filmcraft-cli-media`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-media`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe mediaBrowser.probe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str}
```

## clip.setTimeInterpolation

Set Time Interpolation

- 技能 / Owner: `filmcraft-cli-timeline`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-timeline`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe clip.setTimeInterpolation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clips":[id]?,"mode":"frameSampling|frameBlending|opticalFlow"}
```

## project.searchBinItems

Search Bin Contents

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.searchBinItems`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":id}
```

## project.editSearchBin

Edit Search Bin

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.editSearchBin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":id,"name":str?,"column":str?,"operator":str?,"text":str?,"rows":[..]?,"matchAll":bool?,"caseSensitive":bool?}
```

## project.deleteSearchBin

Delete Search Bin

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe project.deleteSearchBin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"bin":id}
```

## file.templates

List Project Templates

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.templates`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.newProjectFromTemplate

New Project from Template

- 技能 / Owner: `filmcraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.newProjectFromTemplate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"template":name|path,"name":str?}
```

## help.systemReport

System Compatibility Report

- 技能 / Owner: `filmcraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/filmcraft-skills --skill filmcraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe help.systemReport`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```
