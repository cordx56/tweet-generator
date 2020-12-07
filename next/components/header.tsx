import React from 'react';

const Header: React.FC = () => {
  return (
    <div>
      <h1>Tweet generator</h1>
      <p>ツイートを学習して本人っぽい文章を生成するよ！</p>
      <p>マルコフ連鎖によるツイート自動生成プログラム</p>
      <p>
        This program uses
        <span> </span>
        <a
          href="https://github.com/jsvine/markovify"
          target="_blank"
          rel="noreferrer"
        >
          jsvine/markovify
        </a>
      </p>
      <p>
        <strong>
          Detail/Bug report:
          <span> </span>
          <a
            href="https://github.com/cordx56/tweet-generator"
            target="_blank"
            rel="noreferrer"
          >
            cordx56/tweet-generator
          </a>
        </strong>
      </p>
    </div>
  );
};

export default Header;
