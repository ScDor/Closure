import { mount } from '@vue/test-utils'
import App from '@/App.vue'
import { computed, ref, nextTick } from 'vue'


describe('App.vue', () => {

  let isAuthenticated = ref(false)
  const authMock = {
    isAuthenticated: computed(() => isAuthenticated.value),
    loading: computed(() => false)
  }

  const mountOptions = {
      global: {
        mocks: {
          $auth: authMock
        }
      }
  }

  it('contains a login/sign-in string only if not authenicated', async () => {
    const wrapper = mount(App, mountOptions)


    isAuthenticated.value = false
    await nextTick()

    // must contain one of "login", "log-in", "signin", "sign-in", etc..
    const signinRegexMatch = expect.stringMatching(/(sign|log)\W{0,1}in/)
    // must contain one of "logout", "log-out", "signout", "sign-out", etc..
    const signoutRegexMatch = expect.stringMatching(/(sign|log)\W{0,1}out/)
    expect(wrapper.text().toLowerCase()).toEqual(signinRegexMatch)

    isAuthenticated.value = true
    await nextTick()

    console.log(wrapper.text())
    expect(wrapper.text().toLowerCase()).toEqual(signoutRegexMatch)
  })
})
