import Document, { Html, Head, Main, NextScript } from 'next/document';

export default class _Document extends Document {
  render() {
    return (
      <Html lang="en">
        <Head>
          <meta charSet="utf-8" />
          <meta name="theme-color" content="#0a0e27" />
          <meta name="description" content="JARVIS-AI: Autonomous AI Operating System" />
          <link rel="icon" href="/favicon.ico" />
          <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
        </Head>
        <body className="bg-jarvis-dark text-white">
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
