const express = require('express');
const app = express();

app.get('/twitter/callback', (req, res) => {
  // You can access oauth_token and oauth_verifier from the query parameters
  const { oauth_token, oauth_verifier } = req.query;

  if (!oauth_token || !oauth_verifier) {
    return res.status(400).send('Missing oauth_token or oauth_verifier');
  }

  // For now, just respond with the received tokens
  res.send(`Received callback from Twitter!<br>oauth_token: ${oauth_token}<br>oauth_verifier: ${oauth_verifier}`);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Express app listening on port ${PORT}`);
});
