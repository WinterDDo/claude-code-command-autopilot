# Claude Code のための Command Autopilot

**コマンドを一つも覚えずに、Claude Code を 100% 使いこなす。**

[English](README.md) | [中文](README.zh.md) | [Español](README.es.md) | [Português](README.pt.md) | 日本語 | [한국어](README.ko.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

Claude Code を使っているけれど、`/` コマンドには一度も触れたことがない。そんな人のために作りました。「実は取り消せたのに」と知らずに作業を失ったことがある人。計画から始めてほしかった大きな変更に、Claude がいきなり突っ込んでいくのを見ていたことがある人。これは、そんなあなたのためのツールです。

## インストールすると、実際に何が変わるのか

| こんな場面 | Autopilot なし | Autopilot あり |
|---|---|---|
| Claude が何かを壊した | 取り消せることを知らないまま、Claude は「修正」を続ける | まず **/rewind** を差し出してくれる。Esc を 2 回押せば、壊れる前に戻れる |
| 大きな作業を頼んだ | Claude がいきなり編集を始める | **自動で、先に計画を立てる**。あなたが承認するまで何も変更されない |
| セッションの途中で話題を変えた | 古いコンテキストが動作を遅くし、お金も無駄になる | クリックできる選択肢が出る。続行 / まっさらに再開 / 別セッションに分ける。それぞれ理由つき |
| 入れたスキルが眠ったまま | 持っていることすら忘れている | 勝手に使って、報告してくれる。「pdf スキルを使ってファイルを直接読みました」 |
| 同じ提案を何度も無視している | 多くのツールは永遠にしつこい | 空気を読んで静かになる。*あなた* を学習しているから |

Claude Code には約 100 個のスラッシュコマンドが組み込まれていて、さらにあなたがインストールしたスキルもあります。でも初心者はそのほとんどを知りません。だからキー 1 つで巻き戻せたはずの作業を失い、クリアできたはずのコンテキストを浪費し、本当は計画から始めるべき大きな編集に Claude が突っ込んでいくのを、ただ見ているしかないのです。

Command Autopilot は、これを 3 つの動きで解決します。

1. **すすめるのではなく、自分でやる。** Claude が自分でできることは、そのまま実行します。大きな変更はファイルに触れる前に自動でプランモードに入り、あなたの好みはメモリに書き込まれ、インストール済みのスキルはちゃんと使われます(どのスキルが役立ったかは、一行で報告してくれます)。
2. **コマンドは、その瞬間の前に手渡す。後からは渡さない。** あなたにしか押せないコマンド(/rewind、/clear など)は、それが効く分かれ道のまさにその場面で、クリックできる選択肢として届きます。一行のメリット説明つきなので、なぜ押すのかが分かります。
3. **あなたと一緒に進化する。** 提案を受け入れたか、無視したか。そのすべてがローカルに残る証拠になります。Autopilot は空気を読みます。無視され続けた提案は静かになり、役に立った提案はより早く出てくるようになり、だいたい 10 セッションごとに、使い方の記録をあなた専用のルールへと蒸留します。ルールは目に見えて、証拠つきで、削除もできます。

教えるのは **4 つの習慣** だけ(/clear、/btw、/rewind、プランモード)。それぞれ多くても数回伝えたら、あとは静かになります。目指すのは、あなたがその存在を忘れてしまうことです。

## インストール

**いちばん簡単な方法は、Claude にインストールしてもらうことです。** 下のブロックをまるごとコピーして、Claude Code の会話に貼り付けて、Enter を押してください。

```
Command Autopilot プラグインをインストールして:
1. claude CLI の場所を探して。まず `command -v claude` を試して、PATH になければ
   `~/.local/bin/claude`(macOS/Linux でよくある場所)を試して。必要なら以降の手順でフルパスを使って。
2. 実行: claude plugin marketplace add WinterDDo/claude-code-command-autopilot
3. 実行: claude plugin install command-autopilot@claude-code-command-autopilot
4. 両方の成功メッセージを見せて。最後に、Claude Code を完全に終了してから開き直すようリマインドして。
```

インストールは Claude が実行し、CLI が PATH にない場合などの細かい問題も処理してくれます。ターミナルの知識は不要です。

<details>
<summary>手動でインストールする方法</summary>

**ターミナルから:**

```sh
claude plugin marketplace add WinterDDo/claude-code-command-autopilot
claude plugin install command-autopilot@claude-code-command-autopilot
```

`claude` が見つからない場合は、代わりに `~/.local/bin/claude` を使うか、このリポジトリをクローンして `./install.sh` を実行してください。

**Claude Code の CLI セッション内から**(`/plugin` コマンドはデスクトップアプリでは使えません):

```
/plugin marketplace add WinterDDo/claude-code-command-autopilot
/plugin install command-autopilot@claude-code-command-autopilot
```

</details>

そのあと Claude Code を再起動してください(完全に終了すること。フックは起動時に読み込まれます)。2 分ツアーもおすすめです。Claude に「autopilot のツアーをして」と頼んでみてください。

## 2 分で動作を確かめる

1. 大きな作業を頼んでみる。*「このプロジェクトに統計機能を設計して作って」* と言うと、Claude はファイルに触れる前に、**自分からプランモードに入ります**。プランを却下すれば、何も変わっていません。
2. 使い捨てのファイルを作らせてから、*「さっきのを取り消して」* と言ってみる。最初の反応は、上から修正を重ねることではなく、**/rewind(Esc を 2 回)** を差し出すことです。

## 絶対にやらないこと

- **テレメトリなし。** すべての記録はローカルのファイルにあり、自分で開いて、確認して、削除できます。アンインストールすればすべて消えます。
- **しつこくしない。** 固い約束があります。提案は 1 回の返答につき最大 1 つ、同じコマンドは 1 セッションに最大 1 回。「autopilot をミュートして」と一言いえば、静音モードや完全ミュートにできます。無視され続けた提案は、自然に消えていきます。
- **成果を盛らない。** 「autopilot は今まで何をしてくれた?」と聞いてみてください。レポートのすべての数字は、実際に記録されたイベントまでたどれます。

## 正直なコスト

Autopilot は、すべてのプロンプトにルールを注入します。モードによっておよそ 250〜450 トークン(quiet ≈ 230、ミュート = 0)です。これは、確実に効くと実証できた唯一の置き場所のための代償です。ダイヤルはあなたの手の中にあります: `teaching` → `normal` → `quiet` → ミュート。

## クラウドでもチームでも使える

クラウドのセッションは個人設定を読み込みません。そのため、Web 版の Claude Code やチームメイトにも効かせたい場合は、リポジトリの `.claude/settings.json` に以下をコミットしてください(完全なスニペットは [templates/team-settings.json](templates/team-settings.json) にあります)。

```json
{
  "extraKnownMarketplaces": {
    "claude-code-command-autopilot": {
      "source": { "source": "github", "repo": "WinterDDo/claude-code-command-autopilot" }
    }
  },
  "enabledPlugins": { "command-autopilot@claude-code-command-autopilot": true }
}
```

ワークスペースを信頼した全員に、ローカルでもクラウドセッションでも Autopilot が効きます。(クラウドの注意点: 設定の確認プロンプトは表示されないためデフォルト設定が使われ、学習状態はクラウドセッションごとにリセットされます。)

Claude Code をまったく使っていない場合でも大丈夫です。[portable/PROMPT.md](portable/PROMPT.md) を使えば、claude.ai や Cursor など、どんなアシスタントにもコアルールを持ち込めます。貼り付けるだけです。

## 仕組み(興味がある人向け)

1 つの `UserPromptSubmit` フックが、メッセージごとにコンテキストを組み立てます。中身は、標準ルール + あなたが学習させたルール + 圧縮された証拠ダイジェストです。スクリプトがやるのは記録と圧縮だけ。**判断はすべてモデルに任せる** 設計なので、マジックナンバー的なしきい値はどこにもありません。ナレッジベース([commands.json](plugins/command-autopilot/knowledge/commands.json)、[playbooks.json](plugins/command-autopilot/knowledge/playbooks.json))には、全コマンドの一行メリットと 8 つの組み合わせプレイブックが入っていて、モデルが必要なときだけ読むため、プロンプトごとのコストはゼロです。詳しくは [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) をどうぞ。

同梱スキル: `tutor`(ガイドツアー)· `doctor`(動作確認)· `config`(ミュートやモード切替)· `evolve`(証拠をルールに蒸留)· `profile`(価値ダッシュボード)· `whats-new`(新しいコマンドと未使用スキルを、メリットつきで紹介)。

## 動作要件

フル機能には Python 3.8 以上が必要です。Python がなくてもステートレスモードで動きます。コアの動作はそのままで、学習だけが一時停止します。

## よくある質問

**データはどこかに送信されますか?** いいえ。テレメトリはゼロです。すべては `~/.claude/command-autopilot/` のローカルファイルにあり、自分で開いて、確認して、削除できます。アンインストールすればすべて消えます。

**しつこく提案してきませんか?** 固い約束で守られています。提案は 1 回の返答につき最大 1 つ、同じコマンドは 1 セッションに最大 1 回、無視され続けた提案は自然に消えます。「autopilot をミュートして」と言えば、完全に黙ります。

**コストはどれくらいですか?** モードに応じて、メッセージごとにおよそ 250〜450 トークンのルールを注入します(quiet ≈ 230、ミュート = 0)。これは確実に動くことへの正直な代償で、ダイヤルはあなたが握っています。

**Web 版の Claude Code やチームでも使えますか?** はい。リポジトリの `.claude/settings.json` に小さなブロックを 2 つコミットすれば([スニペットはこちら](templates/team-settings.json))、ワークスペースを信頼した全員に効きます。クラウドセッションも含めてです。

**Python が入っていなくても動きますか?** はい、ステートレスモードで動きます。コアの動作はすべて使えて、Python 3.8 以上が用意できるまで、学習レイヤーだけが一時停止します。

**アンインストールするには?** `claude plugin uninstall command-autopilot@claude-code-command-autopilot` を実行して(Claude に頼んでも OK)、`~/.claude/command-autopilot/` を削除してください。何も残りません。

**CLAUDE.md にルールを書くのと、何が違うのですか?** 最初はそれを試しました。2 回も。でも CLAUDE.md のルールは、競合する他の指示に負けてしまいます。プロンプトごとのフック注入だけが、モデルに 100% 届くと実証できた唯一の置き場所でした。この発見と、マジックナンバーなしの学習設計こそが、これが Markdown スニペットではなくプラグインである理由のすべてです。詳しくは [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) をどうぞ。

## コントリビュート

動作はコードではなく、テキストファイルに書かれています。改善のほとんどは `rules/*.txt` の文言修正か、`knowledge/*.json` へのエントリ追加です。改善の進め方は [docs/TUNING.md](docs/TUNING.md) を読み、動作の変更を提案する前に [docs/ACCEPTANCE.md](docs/ACCEPTANCE.md) を実行してください。習慣カードと README の翻訳は、最初の PR としていちばん入りやすいテーマです。

ライセンスは MIT です。
