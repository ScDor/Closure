<template>
  <div class="notification notification-style has-text-centered">
    <label class="menu-label"><b>Sign In</b></label>
    <ul class="menu-list">
      <li class="list-item-style">
        <label class="menu-label">Name</label>

        <div class="field">
          <div class="control">
            <input class="input is-dark" type="text" />
          </div>
        </div>
      </li>

      <li class="list-item-style">
        <label class="menu-label">Huji Mail</label>
        <div class="field has-addons">
          <div class="control is-expanded">
            <input class="input is-dark" type="text" />
          </div>
          <div class="control">
            <a class="button is-static is-small"> @mail.huji.ac.il </a>
          </div>
        </div>
      </li>

      <li class="list-item-style">
        <label class="menu-label">Password</label>
        <div class="field">
          <div class="control">
            <input class="input is-dark" type="text" />
          </div>
        </div>
      </li>

      <li class="list-item-style">
        <label class="menu-label">Track</label>
        <div class="field">
          <div class="control">
            <input class="input is-dark" type="text" />
          </div>
        </div>
      </li>

      <li>
        <p>Already have an account?</p>
      </li>

      <li class="list-item-style">
        <div class="control">
          <button class="button menu-label is-dark">Submit</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style>
/* .notification-style {
  margin-top: 3vh;
  margin-left: auto;
  margin-right: auto;
  min-width: 300px;
  max-width: 30vw;
  min-height: 30vh;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.1);
}

.input {
  display: block;
  padding: 10px 6px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 1px solid #ddd;
  background: transparent;
  box-shadow: 0px 0px 0px;
  border-radius: 0rem;
  color: #555;
}

.is-static {
  border: none;
}

.input:focus {
  box-shadow: none !important;
}

.list-item-style {
  margin: 1.5rem;
} */
</style>