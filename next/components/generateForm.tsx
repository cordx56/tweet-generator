import React, { useState } from 'react';
import { Card, Button, Form } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter } from '@fortawesome/free-brands-svg-icons';
import axios from 'axios';

import { API_BASE_URL } from '../common';

type Props = {
  screen_name?: string;
  onChangeScreenName?: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

const GenerateForm: React.FC<Props> = (props) => {
  const [text, setText] = useState('');
  const [tweetLink, setTweetLink] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const result = (
    <Card border="info">
      <Card.Header className="bg-info text-white">生成結果</Card.Header>
      <Card.Body>
        <Card.Text>
          <p>{text}</p>
          <Button href={tweetLink} target="_blank" variant="primary">
            <FontAwesomeIcon icon={faTwitter} />
            <span> </span>
            ツイート
          </Button>
        </Card.Text>
      </Card.Body>
    </Card>
  );
  const loading = (
    <Card border="secondary">
      <Card.Header className="bg-secondary text-white">読み込み中</Card.Header>
      <Card.Body>
        <Card.Text>生成中</Card.Text>
      </Card.Body>
    </Card>
  );
  const error = (
    <Card border="danger">
      <Card.Header className="bg-danger text-white">エラー</Card.Header>
      <Card.Body>
        <Card.Text>{errorMessage}</Card.Text>
      </Card.Body>
    </Card>
  );

  const handleOnSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setText('');
    setTweetLink('');
    axios
      .get(API_BASE_URL + '/v1/tweetgen/genText/' + props.screen_name, {
        params: {},
      })
      .then((response) => {
        setIsLoading(false);
        if (response.data.status) {
          setText(response.data.text);
          setTweetLink(response.data.tweetLink);
          setErrorMessage('');
        } else {
          setErrorMessage(response.data.message);
        }
      })
      .catch((error) => {
        setIsLoading(false);
        if (error.response) {
          setErrorMessage(error.response.data.message);
        }
      });
  };

  return (
    <div>
      {isLoading && loading}
      {0 < errorMessage.length && error}
      {0 < text.length && result}
      <Form className="mt-3" onSubmit={handleOnSubmit}>
        <Form.Group>
          <Form.Label>アカウント名</Form.Label>
          <Form.Control
            type="text"
            placeholder="@cordx56"
            value={props.screen_name}
            onChange={props.onChangeScreenName}
          />
        </Form.Group>
        <p>オプション</p>
        <Form.Group>
          <Form.Label>長さ</Form.Label>
          <Form.Control type="number" placeholder="最大文字数" />
        </Form.Group>
        <Form.Group>
          <Form.Label>最初の単語</Form.Label>
          <Form.Control type="text" placeholder="開始単語" />
        </Form.Group>
        <Button variant="primary" type="submit">
          生成！
        </Button>
      </Form>
    </div>
  );
};

export default GenerateForm;
