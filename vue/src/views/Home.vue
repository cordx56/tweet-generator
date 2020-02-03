<template lang="pug">
  b-container.home
    h1.my-3 Tweet generator
    p ツイートを学習して本人っぽい文章を生成するよ！
    p マルコフ連鎖によるツイート自動生成プログラム
    p This program uses <a href="https://github.com/jsvine/markovify" target="_blank">jsvine/markovify</a>.
    p Detail/Bug report: <a href="https://github.com/cordx56/tweet-generator" target="_blank">cordx56/tweet-generator</a>.

    b-card(v-if="sentence",header="生成結果",border-variant="info",header-bg-variant="info",header-text-variant="white",align="center")
      b-card-text {{ sentence }}
      b-card-text
        b-button(variant="primary",size="sm",v-bind:href="tweetLink",target="_blank") <font-awesome-icon :icon="['fab', 'twitter']"></font-awesome-icon> ツイート
    b-card(v-if="errorMsg",header="エラー",border-variant="danger",header-bg-variant="danger",header-text-variant="white",align="center")
      b-card-text {{ errorMsg }}
    b-card(v-if="loadingMsg",header="読み込み中",border-variant="secondary",header-bg-variant="secondary",header-text-variant="white",align="center")
      b-card-text {{ loadingMsg }}
    b-card(v-if="$route.query.success",header="学習成功",border-variant="success",header-bg-variant="success",header-text-variant="white",align="center")
      b-card-text {{ $route.query.success }}
      b-card-text いっぱい遊んでいってね。楽しんでもらえたらうれしいな。ほめてもらえるともっとうれしいかも……
    b-card(v-if="$route.query.error",header="学習失敗",border-variant="danger",header-bg-variant="danger",header-text-variant="white",align="center")
      b-card-text {{ $route.query.error }}

    b-form.mt-3(@submit="onGenerate")
      b-form-group(label="アカウント名: ")
        b-form-input(v-model="genForm.screenName",required,placeholder="@cordx56")/
      b-form-group(label="長さ: ")
        b-form-input(v-model="genForm.length",type="number",placeholder="最大文字数")/
      b-form-group(label="最初の単語: ")
        b-form-input(v-model="genForm.startWith",placeholder="開始単語")/
      p
        b-button(type="submit",variant="primary") 生成！

    h2.mt-4 ツイートを学習させる
    p お知らせ: 現在多数の生成リクエストがあり、Twitter APIの制限をかけられている場合があります。生成に失敗する場合、時間をおいてもう一度ご利用ください。
    p
      a(href="/pyapi/tw/authLink?callback=https://markov.cordx.net/pyapi/tw/authAndGen")
        img(src="/resources/sign-in-with-twitter-link.png")/
    p ログインしてツイートを学習させると、あなたや他の人もあなたのツイートを生成して遊べるようになります。
</template>

<script>
export default {
  name: 'home',
  data() {
    return {
      genForm: {
        screenName: this.$route.params.screenName,
        length: '',
        startWith: ''
      },
      sentence: '',
      tweetLink: '',
      errorMsg: '',
      loadingMsg: ''
    }
  },
  methods: {
    onGenerate(evt) {
      evt.preventDefault()
      this.sentence = ""
      this.errorMsg = ""
      this.loadingMsg = "生成中"
      this.genForm.screenName = this.genForm.screenName.startsWith("@") ? this.genForm.screenName.substr(1) : this.genForm.screenName
      this.$axios.post("/pyapi/genText/" + this.genForm.screenName, { length: this.genForm.length, startWith: this.genForm.startWith }).then((response) => {
        if (response.status) {
          this.sentence = response.data.sentence
          this.tweetLink = response.data.tweetLink
        }
        else this.errorMsg = response.data.message
        this.loadingMsg = ""
        this.$router.replace({ path: "/" + this.genForm.screenName })
      }).catch((error) => {
        if (error.response.data && error.response.data.message) this.errorMsg = error.response.data.message
        else this.errorMsg = String(error)
        this.loadingMsg = ""
      })
    }
  }
}
</script>
