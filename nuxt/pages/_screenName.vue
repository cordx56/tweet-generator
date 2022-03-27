<template>
  <b-container class="home">
    <h1 class="my-3">Tweet generator</h1>
    <p>{{ language.match(/ja/) ? 'ツイートを学習して本人っぽい文章を生成するよ！' : 'Learn your tweets and generate tweet like your tweet!' }}</p>
    <p>マルコフ連鎖によるツイート自動生成プログラム</p>
    <p>
      This program uses
      <a href="https://github.com/jsvine/markovify" target="_blank">
        jsvine/markovify</a
      >.
    </p>
    <p>
      <strong>
        Detail/Bug report:
        <span> </span>
        <a href="https://github.com/cordx56/tweet-generator" target="_blank">
          cordx56/tweet-generator</a
        >.
      </strong>
    </p>

    <b-card
      v-if="sentence"
      header="生成結果"
      border-variant="info"
      header-bg-variant="info"
      header-text-variant="white"
      align="center"
    >
      <b-card-text>{{ sentence }}</b-card-text>
      <b-card-text>
        <b-button variant="primary" size="sm" :href="tweetLink" target="_blank">
          <font-awesome-icon :icon="faTwitter"></font-awesome-icon>
          <span> </span>
          Tweet
        </b-button>
      </b-card-text>
    </b-card>
    <b-card
      v-if="errorMsg"
      header="エラー"
      border-variant="danger"
      header-bg-variant="danger"
      header-text-variant="white"
      align="center"
    >
      <b-card-text>{{ errorMsg }}</b-card-text>
    </b-card>
    <b-card
      v-if="loadingMsg"
      header="読み込み中"
      border-variant="secondary"
      header-bg-variant="secondary"
      header-text-variant="white"
      align="center"
    >
      <b-card-text>{{ loadingMsg }}</b-card-text>
    </b-card>
    <b-card
      v-if="$route.query.successfully_generated"
      header="学習成功"
      border-variant="success"
      header-bg-variant="success"
      header-text-variant="white"
      align="center"
    >
      <b-card-text>Successfully Generated!</b-card-text>
      <b-card-text
        >いっぱい遊んでいってね。楽しんでもらえたらうれしいな。ほめてもらえるともっとうれしいかも……</b-card-text
      >
    </b-card>
    <b-card
      v-if="$route.query.successfully_deleted"
      header="成功"
      border-variant="success"
      header-bg-variant="success"
      header-text-variant="white"
      align="center"
    >
      <b-card-text>正常に削除されました。</b-card-text>
    </b-card>
    <b-card
      v-if="$route.query.error_unknown"
      header="失敗"
      border-variant="danger"
      header-bg-variant="danger"
      header-text-variant="white"
      align="center"
    >
      <b-card-text
        >不明なエラーです。しばらくしてからもう一度お試しください。</b-card-text
      >
    </b-card>
    <b-card
      v-if="$route.query.error_24hour_constraint"
      header="失敗"
      border-variant="danger"
      header-bg-variant="danger"
      header-text-variant="white"
      align="center"
    >
      <b-card-text>モデルを生成できるのは24時間に1度のみです。</b-card-text>
    </b-card>
    <b-card
      v-if="$route.query.error_unregistered"
      header="失敗"
      border-variant="danger"
      header-bg-variant="danger"
      header-text-variant="white"
      align="center"
    >
      <b-card-text>未登録です。</b-card-text>
    </b-card>

    <b-form class="mt-3" @submit="onGenerate">
      <b-form-group v-bind:label="language.match(/ja/) ? 'アカウント名' : 'Screen name'">
        <b-form-input
          v-model="genForm.screenName"
          required
          placeholder="@cordx56"
        />
      </b-form-group>
      <b-card
        header="オプション"
        border-variant="secondary"
        header-bg-variant="secondary"
        header-text-variant="white"
        align="center"
      >
        <b-form-group label="長さ">
          <b-form-input
            v-model="genForm.length"
            type="number"
            placeholder="最大文字数"
          />
        </b-form-group>
        <b-form-group label="最初の単語">
          <b-form-input v-model="genForm.startWith" placeholder="開始単語" />
        </b-form-group>
      </b-card>
      <p class="mt-3">
        <b-button type="submit" variant="primary">{{ language.match(/ja/) ? '生成！' : 'Generate!' }}</b-button>
      </p>
    </b-form>

    <h2 class="mt-4">ツイートを学習させる</h2>
    <p>Learn your tweet</p>
    <p>
      <b-button :href="signInLink" variant="primary">
        <font-awesome-icon :icon="faTwitter"></font-awesome-icon>
        <span> </span>
        Sign in with Twitter
      </b-button>
    </p>
    <p>
      ログインしてツイートを学習させると、あなたや他の人もあなたのツイートを生成して遊べるようになります。
    </p>
    <p>
      Once you let us learn your tweet, you and others will be able to generate tweet like your tweet.
    </p>
    <p>
      <b-button variant="danger" size="sm" :href="deleteLink">
        <font-awesome-icon :icon="faTwitter"></font-awesome-icon>
        <span> </span>
        学習削除
      </b-button>
    </p>
    <p>こちらからあなたの学習済みデータを削除することができます。</p>
  </b-container>
</template>

<style>
.home {
  text-align: center;
}
</style>

<script>
import { API_BASE_URL } from '@/common'
import { faTwitter } from '@fortawesome/free-brands-svg-icons'
export default {
  name: 'Home',
  data() {
    return {
      genForm: {
        screenName: this.$route.params.screenName,
        length: '',
        startWith: '',
      },
      sentence: '',
      tweetLink: '',
      errorMsg: '',
      loadingMsg: '',
      signInLink:
        API_BASE_URL +
        '/v1/tweetgen/authRedirect/?callback=' +
        API_BASE_URL +
        '/v1/tweetgen/authAndGen/',
      deleteLink:
        API_BASE_URL +
        '/v1/tweetgen/authRedirect/?callback=' +
        API_BASE_URL +
        '/v1/tweetgen/authAndDel/',
      ranking: [],
      language: '',
    }
  },
  computed: {
    faTwitter() {
      return faTwitter
    },
  },
  mounted() {
    //this.getRanking()
    this.setLanguage()
  },
  methods: {
    onGenerate(evt) {
      evt.preventDefault()
      this.sentence = ''
      this.errorMsg = ''
      this.loadingMsg = '生成中'
      this.genForm.screenName = this.genForm.screenName.startsWith('@')
        ? this.genForm.screenName.substr(1)
        : this.genForm.screenName
      this.$axios
        .get(API_BASE_URL + '/v1/tweetgen/genText/' + this.genForm.screenName, {
          params: {
            length: this.genForm.length,
            startWith: this.genForm.startWith,
          },
        })
        .then((response) => {
          if (response.status) {
            this.sentence = response.data.text
            this.tweetLink = response.data.tweetLink
          } else this.errorMsg = response.data.message
          this.loadingMsg = ''
          this.$router.replace({ path: '/' + this.genForm.screenName })
        })
        .catch((error) => {
          if (error.response && error.response.data.message)
            this.errorMsg = error.response.data.message
          else this.errorMsg = String(error)
          this.loadingMsg = ''
        })
    },
    getRanking() {
      this.$axios
        .get(API_BASE_URL + '/v1/ranking/')
        .then((response) => {
          if (response.status) {
            this.ranking = response.data.ranking
          } else this.errorMsg = response.data.message
        })
        .catch((error) => {
          if (error.response && error.response.data.message)
            this.errorMsg = error.response.data.message
          else this.errorMsg = String(error)
          this.loadingMsg = ''
        })
    },
    setLanguage() {
      this.language = navigator.language
    },
  },
  head() {
    return {
      meta: [
        {
          name: 'twitter:card',
          content: 'summary_large_image',
        },
        {
          name: 'og:title',
          content: 'Tweet generator',
        },
        {
          name: 'og:description',
          content: 'ツイートを自動生成して遊ぼう！',
        },
        {
          name: 'og:image',
          content:
            API_BASE_URL +
            '/v1/tweetgen/genImage/' +
            (this.genForm.screenName ? this.genForm.screenName : ''),
        },
      ],
    }
  },
}
</script>
