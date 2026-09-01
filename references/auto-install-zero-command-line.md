# Auto-Install (Zero Command Line)

When a user asks you to install ai-signal (e.g. "帮我安装 https://github.com/Benboerba620/ai-signal"
or "set up ai signal"), run these steps automatically — the user should NOT need
to touch the terminal:

1. Detect platform and choose install path:
   - FastAgent: `~/.fastagent/skills/ai-signal`（user 层；FastAgent 不扫 `~/.agents/skills/`）
   - OpenClaw: `~/skills/ai-signal`
   - Claude Code: `~/.claude/skills/ai-signal`
   - Other: `~/ai-signal`

2. Install — prefer the package installer, fall back to git clone:
```bash
# 方式一：npx skills 安装器（装到 agent 的 skills 目录，包含完整运行时）
npx skills add tokenaissance/ai-signal

# 方式二：git clone（无 npx 或需要镜像加速时）
git clone https://github.com/Benboerba620/ai-signal.git <install_path>
cd <install_path>/scripts && pip install -r ../requirements.txt
```

   FastAgent 特例：直接把完整包放进 user 层即可被 loader 发现，无需 npx：
```bash
git clone --depth 1 https://github.com/tokenaissance/ai-signal.git ~/.fastagent/skills/ai-signal
```
   （或从 canonical `~/.agents/skills/ai-signal` 复制；装完用 `fastagent skill list` 验证 source=user。）

3. If clone or install fails, diagnose and retry (missing git? missing pip?
   network issue?). Fix it yourself — do not ask the user to run commands.
   If github.com is unreachable (common in mainland China without a proxy),
   retry the clone through a mirror prefix, e.g.
   `git clone https://gh-proxy.com/https://github.com/Benboerba620/ai-signal.git <install_path>`
   or `git clone https://ghfast.top/https://github.com/Benboerba620/ai-signal.git <install_path>`
   (or another gh-proxy-style service if both are down). Daily feed
   fetching does NOT need a proxy afterwards — prepare_digest.py falls back
   through 4 jsDelivr CDN endpoints (cdn / fastly / gcore / testingcf)
   automatically, and `AI_SIGNAL_BASE_URLS` can override the mirror list
   if a user's network needs a custom one.

4. Proceed directly to the Onboarding flow below.

The user's only action is telling you to install. Everything else is your job.

---
