/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */


export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {

    url: 'dev-7k8oa6lt.us.auth0.com', // the auth0 domain prefix
    audience: 'Coffee Shop', // the audience set for the auth0 app
    clientId: 'oB1IuzpABlOSxS902ZfjzR7Ajpfqubt8', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1/login-results', // the base url of the running ionic application. 
    
  }
};
