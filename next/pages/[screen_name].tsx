import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { Container } from 'react-bootstrap';
import Header from '../components/header';
import GenerateForm from '../components/generateForm';
import Learn from '../components/learn';

const ScreenName: React.FC = () => {
  const router = useRouter();
  const { screen_name } = router.query;
  const [screen, setScreen] = useState('');

  useEffect(() => {
    if (screen_name) {
      setScreen(String(screen_name));
    }
  }, [screen_name]);

  return (
    <div className="text-center">
      <Head>
        <title>Tweet generator - {screen_name}</title>
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

export default ScreenName;
