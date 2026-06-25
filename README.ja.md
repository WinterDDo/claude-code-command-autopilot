# Claude Code のための Skill Autopilot

**覚えているスキルだけでなく、インストールしたスキルを使いこなす。**

English | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

<!-- demo: docs/assets/demo.gif embeds here once recorded (LAUNCH §1 storyboard) -->

Claude Code を拡張するためにスキルを入れる。けれど、どれを持っているのか、いつそれが合うのかを忘れてしまう。そして入れれば入れるほど *悪化* します。Claude Code のスキル予算を超えると、いちばん使っていないスキルの説明文が黙って落とされ、*この* タスクにぴったりのスキルがモデルから見えなくなってしまうのです。**Skill Autopilot は、いまあなたがやっていることに最も関連するインストール済みスキルを、毎ターン表に出します。だから、ぴったりの一つが忘れ去られる代わりに、目の前に並びます。** さらに、大きな、あるいはリスクのあるタスクに合う効きの大きい一手(並列エージェント、ワークフロー、自律的な /goal、深いリサーチ)を、あなたが選ぶメニューとして並べ、細かいこと(取り消し、コンテキストの整理)は静かに片づけます。新しく、実験的なものです。オープンソース、MIT、テレメトリなし、ローカルファースト。

## 何ができるようになるのか

| こんな場面 | Autopilot なし | Autopilot あり |
|---|---|---|
| 大きな、複数ファイルにまたがる、あるいは繰り返しの多い作業 | 一歩ずつ手で進めていく | 始める前に **より速い進め方のメニュー** を並べる(並列エージェント、ワークフロー、/background)。トレードオフつきで、あなたが選ぶ |
| 最後まで一気に走らせてよいタスク | 一手ずつお守りをする | **/goal** を差し出し、Claude が自分で最後までやり切る |
| 本格的なリサーチが必要な問い | 浅い検索を 1 回 | **複数ソースの深いリサーチ** を回し、出典つきの答えを返す |
| 入れたのに忘れているスキル | 使われないまま眠っている。あるいは予算を超えるとコンテキストから落とされる | タスクに **関連するものを表に出す**。ぴったりのスキルがモデルの目の前に並ぶ |
| ある提案を断り続けている | 多くのツールは永遠にしつこい | 空気を読んで、その一手は引っ込める。*あなた* を学習しているから |
| 基本(取り消し、コンテキスト、余談) | そのコマンドを覚えたことがない | 静かに処理される。修正の前には **/rewind**、話題の切り替えには **/clear**、余談には **/btw** |

**実際にはこんな感じです:**

```text
You:    add a contacts feature — table, API, form, and tests
Claude: Before I start, a few faster ways to run this — your call:
          1. /goal — I drive it to a finished PR on my own
          2. Parallel agents — build the independent parts at once
          3. Just proceed normally
        (pick one, or say "go")
```

コマンドそのものに初めて触れますか? [プレーンな言葉で書いた Claude Code コマンドチートシート](docs/claude-code-commands-cheatsheet.md)(英語)と [実作業を節約する 8 つの Claude Code ワークフロー](docs/claude-code-workflows.md)(英語)も用意しています。

Claude Code は、あなたがインストールしたスキルとコマンドの上で動きます。けれど、ちょうどいいスキルがちょうどいい瞬間に表に出てくることはめったになく、スキルのライブラリが大きいほど *悪化* します(予算を超えると、Claude Code はいちばん使っていないスキルの説明文をコンテキストから落とすのです)。Skill Autopilot は、そのギャップを 3 つの動きで埋めます。

1. **合うスキルを、合うまさにその時に表に出す。** 毎ターン、インストール済みのスキルを、あなたが実際に頼んでいることと照らしてランク付けし、最も関連するものをモデルの目の前に並べます(名前で。モデルは必要なときに説明文の全文を読みます)。これには、予算超過のせいで Claude Code がコンテキストから落としたスキルも含まれます。そして、大きな、あるいはリスクのあるタスクに、いくつもの効きの大きい一手 — 並列エージェント、ワークフロー、自律的な /goal、深いリサーチ — が合うときは、それらをメニューとして並べ、あなたが選びます。
2. **残りは、すすめるのではなく自分でやる。** Claude が自分でできることは、そのまま実行します。大きな変更はファイルに触れる前にプランモードに入り、好みはメモリに書き込まれ、合うインストール済みのスキルは使われます。安全の基本(/rewind、/clear、/btw)は、説教としてではなく、まさにその瞬間に手渡されます。
3. **あなたの邪魔をしないことを学ぶ。** あなたが見送った提案はすべてローカルの証拠になります。断り続けたものは静かになり、しつこくはなりません。(より深いパーソナライズ、つまり *あなた* が特に好む一手に寄せていくことはロードマップ上にあります。今日の成果は、すでにあなたを分かったふりをすることではなく、的確さと静けさです。)

決まった Tips のチェックリストを上から順に流すことはしません。各ターンについて考え、本当に役立つときだけ、せいぜい一度だけ何かを指摘し、それ以外は静かにしています。目指すのは、あなたがその存在に気づかなくなることです。

**ただ眺めてみたいだけ?** [portable/PROMPT.md](portable/PROMPT.md) を claude.ai でも、どんなアシスタントにでも貼り付けてみてください。コアの動作そのものを、何もインストールせず、60 秒で。

## インストール

**いちばん簡単 — Claude にインストールしてもらう。** このブロックをまるごとコピーして、Claude Code の会話に貼り付け、Enter を押してください:

```
Install the Skill Autopilot plugin for me:
1. Locate my claude CLI: try `command -v claude`; if not on PATH, try `~/.local/bin/claude`
   (the usual macOS/Linux location). Use the full path in the next steps if needed.
2. Run: claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
3. Run: claude plugin install skill-autopilot@claude-code-skill-autopilot
4. Show me both success confirmations, then remind me to fully quit Claude Code, reopen it,
   and run the autopilot doctor to verify.
```

インストールは Claude が実行し、CLI が PATH にない場合などの細かい問題も処理してくれます。ターミナルの知識は不要です。

<details>
<summary>手動でインストールする方法</summary>

**ターミナルから:**

```sh
claude plugin marketplace add WinterDDo/claude-code-skill-autopilot
claude plugin install skill-autopilot@claude-code-skill-autopilot
```

`claude` が見つからない場合は、代わりに `~/.local/bin/claude` を使うか、このリポジトリをクローンして `./install.sh` を実行してください。

**Claude Code の CLI セッション内から**(`/plugin` コマンドはデスクトップアプリでは使えません):

```
/plugin marketplace add WinterDDo/claude-code-skill-autopilot
/plugin install skill-autopilot@claude-code-skill-autopilot
```

</details>

そのあと Claude Code を再起動し(完全に終了すること。フックは起動時に読み込まれます)、Claude に **「autopilot がちゃんと動いているか確認して」** と頼んでください。組み込みの doctor が、すべてが端から端まで発火していることを確認します。それから 2 分ツアーをどうぞ:「autopilot のツアーをして」。

**うまく動かない?**
- 提案がまったく出てこない → 完全に終了して開き直す必要があります。フックは起動時にしか読み込まれません。
- `/plugin` が見つからない → デスクトップアプリには `/plugin` コマンドがありません。上のコピペ式インストールを使ってください。
- それ以外 → Claude に「autopilot doctor を実行して」と頼み、その出力を [issue](https://github.com/WinterDDo/claude-code-skill-autopilot/issues) に貼ってください。

## アップデート

Claude に **「Skill Autopilot プラグインを最新版にアップデートして」** と頼んでください。下の 3 ステップをあなたの代わりに実行します。

手動でやる場合(あるいは「すでに最新版です」と出た場合 — それはローカルのマーケットプレイスのコピーが古いということなので、*まず* リフレッシュしてください):

```sh
claude plugin marketplace update claude-code-skill-autopilot   # refresh the catalog from GitHub
claude plugin update skill-autopilot@claude-code-skill-autopilot
```

そのあと Claude Code を完全に終了して開き直してください。ルールとフックは起動時に読み込まれます。(クラウドセッションは常にリポジトリを新しくクローンするので、新しいバージョンを自分で取り込みます。)

## 2 分で動作を確かめる

1. 大きな作業を頼んでみる: *「このプロジェクトに統計機能を設計して作って。」* → Claude はファイルに触れる前に、**自分からプランモードに入ります**。プランを却下すれば、何も変わっていません。
2. 使い捨てのファイルを作らせてから、*「さっきのを取り消して」* と言ってみる。 → 最初の反応は、上から修正を重ねることではなく、**/rewind(Esc を 2 回)** を差し出すことです。

## 絶対にやらないこと

- **テレメトリなし。** すべての証拠はローカルのファイルにあり、自分で開いて、監査して、削除できます。アンインストールすればすべて消えます。
- **しつこくしない。** 固い約束があります。提案は 1 回の返答につき最大 1 つ、同じコマンドは 1 セッションに最大 1 回。「quiet」や完全ミュートも一言(「mute autopilot」)で済みます。繰り返し却下された提案は、自然にフェードアウトしていきます。
- **成果を盛らない。** 「autopilot は今まで何をしてくれた?」と聞いてみてください。レポートのすべての数字は、実際に記録されたイベントまでたどれます。

## 正直なコスト

Autopilot は、すべてのプロンプトにルールを注入します。定常状態でおよそ 500〜600 トークン(quiet ではより少なく、ミュート時は 0)です。インストール済みのスキルが関連するターンでは、その名前を加えます。小さく上限のある追加分(約 140 トークン)で、上限つき、合うものがないターンでは何も加えません。20 万トークンのコンテキストウィンドウに対しては、コンマ数パーセントです。ダイヤルはあなたの手の中にあります: `teaching` → `normal` → `quiet` → ミュート。

## クラウドでもチームでも使える

クラウドのセッションは個人のプラグインを読み込まず、マーケットプレイスのキャッシュもリフレッシュしません。そのため、Web 版の Claude Code やチームメイトにも確実に Autopilot を効かせる方法は、**そのルールをリポジトリにベンダリングすること** です。小さな `.claude/autopilot-context.json`(ルール)に加えて `.claude/autopilot-cloud.sh` をコミットし、リポジトリの `.claude/settings.json` で `SessionStart` + `UserPromptSubmit` フックをそこに紐づけます。このリポジトリのクローンから、1 つのコマンドでファイルをコピーし、正確なフックの行を表示できます:

```sh
plugins/skill-autopilot/scripts/vendor-to-repo.sh /path/to/your/repo
# then paste the printed hook lines into /path/to/your/repo/.claude/settings.json and commit
```

新しいクラウドセッションはあなたのリポジトリを新しくクローンするので、ルールを自動的に取り込みます。そのリポジトリで作業する全員にです。(クラウドの注意点: そこでの学習状態はセッションごとです。その瞬間のメニューはそれでも機能します。)

## 仕組み(興味がある人向け)

1 つの `UserPromptSubmit` フックが、メッセージごとにコンテキストを組み立てます。中身は、短い思考の規律 + あなたのプロンプトに最も関連するインストール済みスキル + あなたが学習させたルール + 圧縮された証拠ダイジェストです。スキルを表に出す仕組みは、あえて素朴で正直です。セッション開始時にインストール済みスキルのローカルなインデックスを作り、毎ターン、あなたのプロンプトとの安価な単語の重なりでランク付けし、最も関連する数個の *名前* だけを注入します(モデルは必要なときに各説明文の全文を読み、使うかどうかを判断します)。合うものがなければ何も注入しません。**シナリオ→コマンドの対応表はありません** し、モデルに信用しろと教える類似度スコアラーもありません。モデルは毎ターン、*あなたの* タスクが何を必要としているかを新たに考えます。ナレッジベースはトリガーではなく参照用です。スクリプトがやるのは記録と圧縮だけ — **判断はすべてモデルに委ねられている** ので、どこにもマジックナンバー的なしきい値はありません。ナレッジベース([commands.json](plugins/skill-autopilot/knowledge/commands.json)、[playbooks.json](plugins/skill-autopilot/knowledge/playbooks.json))には、全コマンドの一行メリットと一連の組み合わせプレイブックが入っていて、モデルが必要なときだけ読むため、プロンプトごとのコストはゼロです。詳しくは [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) をどうぞ。

同梱スキル: `tutor`(ガイドツアー)· `doctor`(動作確認)· `config`(ミュートやモード切替)· `evolve`(あなたの証拠をルールに蒸留)· `profile`(価値ダッシュボード)· `whats-new`(新しいコマンドと未使用スキルを、メリットつきで紹介)。

## 動作要件

フル機能には Python 3.8 以上が必要です。Python がなくても、Autopilot はステートレスモードで動きます。コアの動作はそのままで、学習だけが一時停止します。

## よくある質問

**データはどこかに送信されますか?** いいえ。テレメトリはゼロです。すべては `~/.claude/command-autopilot/` のローカルファイルにあり、自分で開いて、監査して、削除できます。アンインストールすればすべて消えます。

**何か隠していませんか?** いいえ。Claude に「何があなたを導いているの?」と聞くか、このプラグインが注入している指示を見せてと頼めば、すべてを教えてくれます。ルールは [`plugins/skill-autopilot/rules/`](plugins/skill-autopilot/rules) にプレーンテキストで置かれていて、ガイダンスは Claude に対して、あなたが尋ねたらいつでも透明であるよう明示的に指示しています。このプラグインに、あなたから見て秘密のものは何もありません。

**しつこく提案してきませんか?** 固い約束で「いいえ」と決まっています。提案は 1 回の返答につき最大 1 つ、同じコマンドは 1 セッションに最大 1 回、却下し続けた提案は自然に消えます。「mute autopilot」と言えば、完全に黙ります。

**コストはどれくらいですか?** 定常状態で、メッセージごとにおよそ 500〜600 トークンのルール(quiet ではより少なく、ミュート時は 0)に加えて、インストール済みのスキルが関連するターンでは小さく上限のある追加分(約 140 トークン)です。20 万トークンのウィンドウのコンマ数パーセントです。ダイヤルはあなたが握っています。

**Web 版の Claude Code やチームでも使えますか?** はい。1 つのコマンド(`vendor-to-repo.sh`、[クラウドでもチームでも使える](#クラウドでもチームでも使える)を参照)で、そのルールをリポジトリの `.claude/` にベンダリングします。クラウドセッションはリポジトリを新しくクローンして取り込むので、そのリポジトリで作業する全員に効きます。

**Python が入っていなくても動きますか?** はい、ステートレスモードで動きます。コアの動作はすべて使えて、Python 3.8 以上が用意できるまで、学習レイヤーだけが一時停止します。

**アンインストールするには?** `claude plugin uninstall skill-autopilot@claude-code-skill-autopilot` を実行して(Claude に頼んでも OK)、`~/.claude/command-autopilot/` を削除してください。何も残りません。

**CLAUDE.md にルールを書くのと、何が違うのですか?** 最初はそれを試しました。2 回も。でも CLAUDE.md のルールは、競合する他の指示に負けてしまいます。プロンプトごとのフック注入だけが、モデルに 100% 届くと実証できた唯一の置き場所でした。この発見と、マジックナンバーなしの学習設計こそが、これが Markdown スニペットではなくプラグインである理由のすべてです。詳しくは [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) をどうぞ。

## コントリビュート

**5 分で最初の PR:** `plugins/skill-autopilot/rules/*.txt` のどれか 1 つの提案の文言を改善するか、`plugins/skill-autopilot/knowledge/commands.json` にコマンドの一行メリットを追加し、[docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) の対応するステップを実行して、提出してください。README の翻訳も同じくらい歓迎です。動作はコードではなくテキストファイルにあります。反復の進め方については [docs/TUNING.md](docs/TUNING.md) をご覧ください。

ライセンスは MIT です。
