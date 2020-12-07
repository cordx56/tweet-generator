import React, { useState } from 'react';
import Head from 'next/head';
import { Container } from 'react-bootstrap';
import Header from '../components/header';
import GenerateForm from '../components/generateForm';
import Learn from '../components/learn';

const Home: React.FC = () => {
  const [screen, setScreen] = useState('');
  return (
    <div className="text-center">
      <Head>
        <title>Tweet generator</title>
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
