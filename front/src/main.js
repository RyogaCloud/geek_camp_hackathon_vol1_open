import Vue from "vue";
import App from "./App.vue";
import firebase from "firebase";

const config = {
  apiKey: "AIzaSyAzox-yCigtLo3KLEg9OjSbSb1iMweKMFU",
  authDomain: "geekcamphackathon-vol1.firebaseapp.com",
  databaseURL: "https://geekcamphackathon-vol1-default-rtdb.firebaseio.com",
  projectId: "geekcamphackathon-vol1",
  storageBucket: "geekcamphackathon-vol1.appspot.com",
  messagingSenderId: "267679852992",
  appId: "1:267679852992:web:ad61f138cc5300061cc025",
};

firebase.initializeApp(config);

Vue.config.productionTip = false;

new Vue({
  render: (h) => h(App),
}).$mount("#app");
