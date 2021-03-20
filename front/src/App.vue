<template>
  <div id="app">
    <div
      class="modal_container"
      :class="{ 'is-open': tabSelect.isTxt }"
      @click.self="inputTxt_change()"
    >
      <div class="modal_main_container modal_main_text">
        <div class="form_container">
          <h3>自由引数の入力</h3>
          <p>ディレクトリなどの引数を任意文字列にてご入力ください</p>
          <p>例) ~/usr/exapmle/desktop など</p>
          <input class="form_input" type="text" v-model="FreeText" />
        </div>
        <div class="enroll_btn" @click="inputTxt_Add()">追加</div>
      </div>
    </div>
    <div
      class="modal_container"
      :class="{ 'is-open': tabSelect.isUsrEnroll }"
      @click.self="user_enroll_cmd()"
    >
      <div class="modal_main_container modal_main_usrenroll">
        <div class="form_container">
          <h3>カスタムコマンドの入力</h3>
          <p>標準コマンド以外をご利用になる場合はご入力ください</p>
          <p>例) docker-compose など</p>
          <input class="form_input" type="text" v-model="userEnrollcommand" />
        </div>
        <div class="enroll_btn" @click="custumCommandAdd()">追加</div>
      </div>
    </div>
    <div id="header_container">
      <div id="search_container">
        <div id="search_border">
          <input type="text" id="search_box" placeholder="Search command..." v-model="searchWord"/>
          <div id="search_button_container" @click="searchcommands">
            <img id="search_button" src="./assets/search_button.png" alt="">
          </div>
        </div>
      </div>
      <div id="title_container">
        <img
          src="./assets/logo.png"
          alt=""
          style="width: 170px; user-select: none"
        />
      </div>
      <div v-if="isLogin" class="auth_container">
          <img style="width:50px; margin-right: 15px; border-radius: 15px;" v-bind:src="authUserIcon" alt="">
          <div class="auth_button" style="background: #F45363" @click="signOut">ログアウト</div>
      </div>
      <div v-else class="auth_container">  
        <div class="auth_button" @click="signIn">ログイン</div>
      </div>
    </div>
    <div id="main_container">
      <div id="tab_container">
        <div
          class="tab tab_cmd"
          @click="tabClicked('cmd')"
          :class="{ 'is-selected': tabSelect.isCmd }"
        >
          >_
        </div>
        <div
          v-if="optTabDisp"
          class="tab tab_option"
          @click="tabClicked('opt')"
          :class="{ 'is-selected': tabSelect.isOpt }"
        >
          -a
        </div>
        <div
          v-if="isLogin"
          class="tab tab_usr"
          @click="tabClicked('usr')"
          :class="{ 'is-selected': tabSelect.isUsr }"
        >
          @
        </div>
        <div v-if="isLogin" class="tab tab_usr_enroll" @click="user_enroll_cmd()">->@</div>
        <div class="tab tab_txt" @click="inputTxt_change()">txt_</div>
      </div>
      <div id="cmds_container">
        <div id="cmds_border">
          <div class="tab_element" v-if="tabSelect.isCmd">
            <div
              v-for="(command, tab_cmd_index) in commands"
              v-bind:key="tab_cmd_index"
              :class="'type_' + command.type"
              class="cmd_tile_container cmd_insert"
              @click="commandsAdd(command)"
            >
              {{ command.label }}
            </div>
          </div>
          <div class="tab_element" v-else-if="tabSelect.isOpt">
            <div
              v-for="(option, tab_opt_index) in optionsList"
              v-bind:key="tab_opt_index"
              :class="'type_' + option.type"
              class="cmd_tile_container cmd_insert"
              @click="commandsAdd(option)"
            >
              {{ option.label }}
            </div>
          </div>
          <div class="tab_element" v-if="tabSelect.isUsr">
            <div
              v-for="(user, tab_usr_index) in users"
              v-bind:key="tab_usr_index"
              :class="'type_' + user.type"
              class="cmd_tile_container cmd_insert"
              @click="commandsAdd(user)"
            >
              {{ user.label }}
            </div>
          </div>
        </div>
      </div>
      <div id="edit_container">
        <div id="edit_border">
          <div
            class="edit_vertical"
            v-for="(editData, index) in editDatas"
            v-bind:key="index"
          >
            <div :class="'type_' + editData.type" class="cmd_tile_container">
              {{ editData.label }}
              <div class="remove" @click="commandsRemove([index])">×</div>
            </div>
            <div
              v-for="(edit_option, edit_opt_index) in editData.options"
              v-bind:key="edit_opt_index"
              :class="'type_' + edit_option.type"
              class="cmd_tile_container"
            >
              {{ edit_option.label }}
              <div
                class="remove"
                @click="commandsRemove([index, edit_opt_index])"
              >
                ×
              </div>
            </div>
          </div>
        </div>
        <div id="result_container">
          <div id="preview_container">
            #!/bin/bash
            <div
              class="preview_vertical"
              v-for="(editData, index) in editDatas"
              v-bind:key="index"
            >
              {{ editData.label }}
              <div
                style="margin-left: 15px"
                v-for="(edit_option, edit_opt_index) in editData.options"
                v-bind:key="edit_opt_index"
              >
                {{ edit_option.label }}
              </div>
            </div>
          </div>
          <div id="genelate_btn_container">
            <div id="genelate_btn" @click="handleDownload()">DOWNLOAD</div>
          </div>
        </div>
      </div>
    </div>
    <div ref="drag"></div>
  </div>
</template>

<script>
import firebase from "firebase";

export default {
  name: "App",
  data() {
    return {
      isLogin:false,
      authUserIcon:"",
      authUid:"",
      searchWord:"",
      FreeText: "",
      userEnrollcommand:"",
      optTabDisp:false,
      tabSelect: {
        isCmd: true,
        isOpt: false,
        isUsr: false,
        isUsrEnroll: false,
        isTxt: false,
      },
      isLoginModal: false,
      editDatas: [],
      spare_commands: [],
      commands: [],
      optionsList: [],
      users: [
        {
          label: "docker",
          type: "usr",
          options: [],
        },
        {
          label: "docker-compose",
          type: "usr",
          options: [],
        },
        {
          label: "nano",
          type: "usr",
          options: [],
        },
      ],
    };
  },
  methods: {
    custumCommandAdd(){
      firebase.database().ref(this.authUid + "/" + this.userEnrollcommand)
        .set({
          label:this.userEnrollcommand
        });
      this.userEnrollcommand = "";
      this.tabSelect.isUsrEnroll = !this.tabSelect.isUsrEnroll;
    },
    signIn() {
      const provider = new firebase.auth.GoogleAuthProvider();
      firebase
        .auth()
        .signInWithPopup(provider)
        .then(user => {
          if (user) {
            // !!userはBoolen変更後反転
            this.isLogin = !!user;
            this.authUserIcon = user.photoURL;
            this.authUid = user.uid
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    signOut() {
      firebase.auth().signOut();
      this.isLogin = false;
      this.authUid = ""
    },
    searchcommands(){
      let target = this.searchWord;
      if(target == ""){
        return
      }
      this.tabSelect.isOpt = false;
      this.tabSelect.isUsr = false;
      this.tabSelect.isCmd = true;
      fetch('fetchURL', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + btoa('APITOKEN')
        },
        body: JSON.stringify({"text": target})
      })
        .then(response =>  {
            return response.json();
        }).then( res => {
          let commands = res.response.result.commands;
          this.commands = commands
        }).catch(function (error) {
            console.log(error);
            
        });
    },
    inputTxt_change() {
      this.FreeText = "";
      this.tabSelect.isTxt = !this.tabSelect.isTxt;
    },
    inputTxt_Add() {
      if (this.editDatas.length) {
        this.editDatas[this.editDatas.length - 1].options.push(
          JSON.parse(
            JSON.stringify({
              label: this.FreeText,
              type: "text",
            })
          )
        );
      } else {
        console.log("コマンド未入力でオプション入力をされました");
      }
      this.FreeText = "";
      this.tabSelect.isTxt = !this.tabSelect.isTxt;
    },
    user_enroll_cmd() {
      this.tabSelect.isUsrEnroll = !this.tabSelect.isUsrEnroll;
    },
    tabClicked(tabClick) {
      if (tabClick == "cmd") {
        this.tabSelect.isOpt = false;
        this.tabSelect.isUsr = false;
        this.tabSelect.isCmd = true;
        this.commands = this.spare_commands;
      } else if (tabClick == "opt") {
        this.tabSelect.isUsr = false;
        this.tabSelect.isCmd = false;
        this.tabSelect.isOpt = true;
      } else {
        this.tabSelect.isCmd = false;
        this.tabSelect.isOpt = false;
        this.tabSelect.isUsr = true;
      }
    },
    commandsAdd(target) {
      if (target.type == "opt") {
        if (this.editDatas.length) {
          this.editDatas[this.editDatas.length - 1].options.push(
            JSON.parse(JSON.stringify(target))
          );
        } else {
          console.log("コマンド未入力でオプション入力をされました");
        }
      } else if (target.type == "usr"){
        if(!this.editDatas.length){
          this.optTabDisp = true;
        }
        this.editDatas.push(JSON.parse(JSON.stringify(target)));
        this.optionsList = target.optionsList;
        this.tabSelect.isUsr = true;
        this.tabSelect.isCmd = false;
        this.tabSelect.isOpt = false;
      } else {
        if(!this.editDatas.length){
          this.optTabDisp = true;
        }
        this.editDatas.push(JSON.parse(JSON.stringify(target)));
        this.optionsList = target.optionsList;
        this.tabSelect.isUsr = false;
        this.tabSelect.isCmd = false;
        this.tabSelect.isOpt = true;
      }
    },
    commandsRemove(target) {
      if (target.length == 1) {
        this.editDatas.splice(target[0], 1);
        if(!this.editDatas.length){
          this.optTabDisp = false;
          this.tabSelect.isOpt = false;
          this.tabSelect.isUsr = false;
          this.tabSelect.isCmd = true;
        }
      } else if (target.length == 2) {
        this.editDatas[target[0]].options.splice(target[1], 1);
      } else {
        console.log("間違えたremoveクリック");
      }
    },
    handleDownload() {
      var contents = ["#!/bin/bash\n"];
      for (var elem_label of this.editDatas) {
        var content = "";
        content = elem_label.label;
        if (elem_label.options) {
          for (var elem_option of elem_label.options) {
            content += " " + elem_option.label;
          }
        }
        contents.push(content + "\n");
      }
      var blob = new Blob(contents, { type: "text/plain" });
      let link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = "shell-io.sh";
      link.click();
    },
  },
  mounted: function() {
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        // !!userはBoolen変更後反転
        this.isLogin = !!user;
        this.authUserIcon = user.photoURL;
        this.authUid = user.uid
        firebase.database().ref(this.authUid).on("value", (customCmd) =>{
          this.users = [];
          let prepare;
          let customCmdList = customCmd.val();
          for (let cmd of Object.keys(customCmdList)) {
            prepare = {
              label: cmd,
              type: "usr",
              options: [],
            };
            this.users.push(prepare);
          }
        });
      }
    });
    
  },
  created() {
    firebase
      .database()
      .ref("general")
      .once("value", (rawdata) => {
        this.commands = [];
        let prepare;
        let cmds = JSON.parse(JSON.stringify(rawdata.val()));
        for (let cmd of Object.keys(cmds)) {
          prepare = {
            description: "",
            label: "",
            options: [],
            optionsList: [],
            type: "cmd",
          };
          for (let opt of Object.keys(cmds[cmd])) {
            // キーとキー配下の値が同じであればそれがコマンド
            if (cmd == opt) {
              prepare.description = cmds[cmd][opt]["description"];
              prepare.label = cmd;
            } else {
              prepare.optionsList.push({
                description: cmds[cmd][opt]["description"],
                label: opt,
                type: cmds[cmd][opt]["type"],
              });
            }
          }
          this.commands.push(prepare);
        }
        this.spare_commands = this.commands;
      });
  },
};
</script>

<style lang="scss">
input[type="text"]:focus {
  outline: 0;
}
img {
  pointer-events: none;
}
#app {
  width: 100vw;
  height: 100vh;
  background-color: #e4ecfc;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-direction: column;
  #header_container {
    width: 100%;
    height: 8vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
    #search_container {
      width: 25%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      #search_border {
        width: 80%;
        height: 60%;
        padding: 5px 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: row;
        border-radius: 15px;
        background: #e4ecfc;
        box-shadow: 5px 5px 10px #abb1bd, -5px -5px 10px #ffffff;
        #search_box {
          width: 80%;
          height: 100%;
          padding: 0 10px;
          margin-left: 5px;
          margin-right: 10px;
          border-radius: 10px;
          border: none;
          background: #e4ecfc;
          box-shadow: inset 2px 2px 5px #abb1bd, inset -2px -2px 5px #ffffff;
        }
        #search_button_container{
          cursor: pointer;
          width: 12%;
          padding: 3px;
          border-radius: 10px;
          border: solid 1px #777777;
          box-shadow: 5px 5px 10px #abb1bd, -5px -5px 10px #ffffff;
          &:hover{
            box-shadow: inset 2px 2px 5px #abb1bd, inset -2px -2px 5px #ffffff;
          }
          #search_button{
            width: 100%;
            height: 100%;
          }
        }
      }
    }
    #title_container {
      width: 55%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .auth_container {
      width: 20%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: row;
      .auth_button {
        user-select: none;
        cursor: pointer;
        width: 60%;
        height: 60%;
        margin: 6px 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 10px;
        background-color: #2e7afc;
        color: #ffffff;
        box-shadow: 0px 4px 8px 0 rgb(0 0 0 / 12%),
          0px 2px 4px 0 rgb(0 0 0 / 8%);
        &:hover {
          box-shadow: 0 0 0 #abb1bd, 0 0 0 #ffffff;
        }
      }
    }
  }
  #main_container {
    width: 100vw;
    height: 90vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
    #tab_container {
      width: 5%;
      height: 100%;
      display: flex;
      justify-content: flex-start;
      align-items: center;
      flex-direction: column;
      .tab {
        user-select: none;
        cursor: pointer;
        width: 50px;
        height: 50px;
        border-radius: 50px;
        margin: 10px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 5px 5px 10px #abb1bd, -5px -5px 10px #ffffff;
      }
      .tab_cmd {
        background: #e4ecfc;
        &.is-selected {
          background: #65bd43;
          color: #fefefe;
        }
        &:hover {
          background: #65bd43;
          color: #fefefe;
        }
      }
      .tab_option {
        background: #e4ecfc;
        &.is-selected {
          background: #e65358;
          color: #fefefe;
        }
        &:hover {
          background: #e65358;
          color: #fefefe;
        }
      }
      .tab_usr {
        background: #e4ecfc;
        &.is-selected {
          background: #6c30f1;
          color: #fefefe;
        }
        &:hover {
          background: #6c30f1;
          color: #fefefe;
        }
      }
      .tab_usr_enroll {
        margin-top: 40px;
        border-radius: 5px;
        background: #e4ecfc;
        &:hover {
          background: #6c30f1;
          color: #fefefe;
        }
      }
      .tab_txt {
        border-radius: 5px;
        background: #e4ecfc;
        &:hover {
          background: #2e7afc;
          color: #fefefe;
        }
      }
    }
    #cmds_container {
      width: 20%;
      height: 100%;
      padding: 15px;
      border-radius: 15px;
      background: #e4ecfc;
      box-shadow: 5px 5px 10px #abb1bd, -5px -5px 10px #ffffff;
      #cmds_border {
        width: 100%;
        height: 100%;
        border-radius: 10px;
        background: #e4ecfc;
        box-shadow: inset 3px 3px 7px #abb1bd, inset -3px -3px 7px #ffffff;
        .tab_element {
          width: 100%;
          height: 100%;
          padding: 5px 10px;
          border-radius: 5px;
          display: flex;
          justify-content: flex-start;
          align-items: flex-start;
          flex-direction: column;
          overflow-y: scroll;
        }
      }
    }
    #edit_container {
      width: 75%;
      height: 100%;
      padding: 15px;
      margin: 15px;
      border-radius: 15px;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: row;
      background: #e4ecfc;
      box-shadow: 5px 5px 10px #abb1bd, -5px -5px 10px #ffffff;
      #edit_border {
        width: 40%;
        height: 100%;
        padding: 5px 10px;
        margin: 5px;
        border-radius: 5px;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        flex-direction: column;
        overflow-y: scroll;
        background: #e4ecfc;
        box-shadow: inset 3px 3px 7px #abb1bd, inset -3px -3px 7px #ffffff;
        .edit_vertical {
          width: 100%;
          margin: 15px 0;
          display: flex;
          justify-content: flex-start;
          align-items: flex-start;
          flex-direction: row;
          flex-wrap: wrap;
        }
      }
      #result_container {
        height: 100%;
        width: 60%;
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        flex-direction: column;
        #preview_container {
          user-select: none;
          width: 100%;
          height: 90%;
          padding: 5px 10px;
          margin: 5px;
          border-radius: 5px;
          display: flex;
          justify-content: flex-start;
          align-items: flex-start;
          flex-direction: column;
          overflow-y: scroll;
          background: #ececf4;
          box-shadow: inset 2px 2px 5px #c9c9cf, inset -2px -2px 5px #ffffff;
          .preview_vertical {
            width: 100%;
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
            flex-direction: row;
            flex-wrap: wrap;
          }
        }
        #genelate_btn_container {
          width: 100%;
          height: 10%;
          display: flex;
          justify-content: center;
          align-items: center;
          #genelate_btn {
            user-select: none;
            cursor: pointer;
            width: auto;
            height: auto;
            padding: 10px 40px;
            background: #0a847a;
            border-radius: 15px;
            color: #fefefe;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 5px 5px 10px #abb1bd, -5px -5px 10px #ffffff;
            &:hover {
              box-shadow: 0 0 0 #abb1bd, 0 0 0 #ffffff;
            }
          }
        }
      }
    }
  }
}
.modal_container {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  overflow-y: auto;
  visibility: hidden;
  background: #22222277;
  z-index: -1;
  display: flex;
  justify-content: center;
  align-items: center;
  &.is-open {
    visibility: visible;
    opacity: 1;
    z-index: 100;
  }
  .modal_main_container {
    min-width: 600px;
    min-height: 400px;
    width: 50%;
    height: 50%;
    padding: 15px;
    border-radius: 15px;
    background-color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    .form_container {
      width: 50%;
      height: auto;
      margin-bottom: 40px;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      .form_input {
        width: 400px;
        height: 30px;
        border-radius: 15px;
        padding: 5px 10px;
        margin-top: 20px;
      }
    }
    .enroll_btn {
      user-select: none;
      cursor: pointer;
      width: auto;
      height: auto;
      padding: 10px 40px;
      background: #045c44;
      border-radius: 15px;
      color: #fefefe;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 5px 5px 10px #abb1bd, -5px -5px 10px #ffffff;
      &:hover {
        box-shadow: 0 0 0 #abb1bd, 0 0 0 #ffffff;
      }
    }
  }
  .modal_main_text {
    border: solid 5px #2e7afc;
  }
  .modal_main_login {
    border: solid 5px #2e7afc;
  }
  .modal_main_usrenroll {
    border: solid 5px #6c30f1;
  }
}
.cmd_tile_container {
  user-select: none;
  width: auto;
  height: 35px;
  padding: 5px 20px;
  margin: 7px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  border-radius: 10px;
  box-shadow: 5px 5px 10px #abb1bd, -5px -5px 10px #ffffff;
  .remove {
    cursor: pointer;
    width: 20px;
    height: 20px;
    border-radius: 5px;
    background: #f4fcf5;
    margin-left: 20px;
    color: #ec2b2d;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 17px;
  }
}
.cmd_insert {
  cursor: pointer;
  &:hover {
    box-shadow: 0px 0px 0px;
  }
}
.type_cmd {
  background: #65bd43;
  color: #fefefe;
}
.type_opt {
  background: #e65358;
  color: #fefefe;
}
.type_usr {
  background: #6c30f1;
  color: #fefefe;
}
.type_text {
  background: #2e7afc;
  color: #fefefe;
}
.box_placeholder {
  width: 100%;
  margin: 7px;
  border-radius: 10px;
  background: #d4dcec;
}
.clone_element {
  --tw-translate-x: 0;
  --tw-translate-y: 0;
  --tw-rotate: 0;
  --tw-skew-x: 0;
  --tw-skew-y: 0;
  --tw-scale-x: 1;
  --tw-scale-y: 1;
  transform: translateX(var(--tw-translate-x)) translateY(var(--tw-translate-y))
    rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y))
    scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));
  --tw-rotate: 12deg;
}
/* A Modern CSS Reset */
*,
*::before,
*::after {
  box-sizing: border-box;
}
body,
h1,
h2,
h3,
h4,
p,
figure,
blockquote,
dl,
dd {
  margin: 0;
}
ul[role="list"],
ol[role="list"] {
  list-style: none;
}
html:focus-within {
  scroll-behavior: smooth;
}
body {
  min-height: 100vh;
  text-rendering: optimizeSpeed;
  line-height: 1.5;
}
a:not([class]) {
  text-decoration-skip-ink: auto;
}
img,
picture {
  max-width: 100%;
  display: block;
}
input,
button,
textarea,
select {
  font: inherit;
}
@media (prefers-reduced-motion: reduce) {
  html:focus-within {
    scroll-behavior: auto;
  }
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
</style>
