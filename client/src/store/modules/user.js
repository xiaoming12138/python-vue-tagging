import Cookies from 'js-cookie';

const user = {
  state: {
    user: '',
    email: '',
  }
}
moutations: {
  SET_USER: (state, type) => {
    state.user = type;
  }
  SET_EMAIL: (state, type) => {
    state.email = type;
  }
}
