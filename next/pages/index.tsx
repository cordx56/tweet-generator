import React, { useState } from 'react';
import Head from 'next/head';
import { Container } from 'react-bootstrap';
import Header from '../components/header';
import GenerateForm from '../components/generateForm';
import Learn from '../components/learn';
import { API_BASE_URL } from '../common';

const Home: React.FC = () => {
  const [screen, setScreen] = useState('');
  return (
    <div className="text-center">
      <Head>
        <title>Tweet generator</title>
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="og:title" content="Tweet generator" />
        <meta name="og:description" content="ツイートを自動生成して遊ぼう！" />
        <meta
          name="og:image"
          content={API_BASE_URL + '/v1/tweetgen/genImage/'}
        />
      </Head>
      <Container>
        <Header />
        <GenerateForm
          screen_name={screen}
          onChangeScreenName={(e) => setScreen(e.target.value)}
        />
        <Learn />
      </Container>
    </div>
  );
};

export default Home;
