import React from 'react';
import { Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter } from '@fortawesome/free-brands-svg-icons';
import { API_BASE_URL } from '../common';

const Learn: React.FC = () => {
  return (
    <div>
      <h1 className="mt-3">ツイートを学習させる</h1>
      <p>
        <Button
          variant="primary"
          href={
            API_BASE_URL +
            '/v1/tweetgen/authRedirect/?callback=' +
            API_BASE_URL +
            '/v1/tweetgen/authAndGen/'
          }
        >
          <FontAwesomeIcon icon={faTwitter} />
          <span> </span>
          Sign in with Twitter
        </Button>
      </p>
      <p>
        ログインしてツイートを学習させると、あなたや他の人もあなたのツイートを生成して遊べるようになります。
      </p>
      <p>
        <Button
          variant="danger"
          href={
            API_BASE_URL +
            '/v1/tweetgen/authRedirect/?callback=' +
            API_BASE_URL +
            '/v1/tweetgen/authAndDel/'
          }
        >
          <FontAwesomeIcon icon={faTwitter} />
          <span> </span>
          学習削除
        </Button>
      </p>
    </div>
  );
};

export default Learn;
