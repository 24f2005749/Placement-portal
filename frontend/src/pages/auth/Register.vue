<template>

    <AuthLayout>

        <div class="card shadow p-4" style="width:450px;">

            <h3 class="text-center mb-4">

                Register

            </h3>

            <form @submit.prevent="register">

                <div class="mb-3">

                    <label>Email</label>

                    <input v-model="email" type="email" class="form-control" required>

                </div>

                <div class="mb-3">

                    <label>Password</label>

                    <input v-model="password" type="password" class="form-control" required>

                </div>

                <div class="mb-3">

                    <label>Role</label>

                    <select v-model="role" class="form-select" required>

                        <option value="">Select Role</option>
                        <option value="student">Student</option>
                        <option value="company">Company</option>

                    </select>

                </div>

                <button class="btn btn-primary w-100">

                    Register

                </button>

            </form>

            <div v-if="error" class="alert alert-danger mt-3">

                {{ error }}

            </div>

            <p class="text-center mt-3">

                Already have an account?

                <router-link to="/login">

                    Login

                </router-link>

            </p>

        </div>

    </AuthLayout>

</template>

<script>

import api from "@/services/api"
import AuthLayout from "@/layouts/AuthLayout.vue"

export default {

    components: { AuthLayout },

    data() {

        return {

            email: "",
            password: "",
            role: "",
            error: ""

        }

    },

    methods: {

        async register() {

            this.error = ""

            try {

                const response = await api.post("/register", {

                    email: this.email,
                    password: this.password,
                    role: this.role

                })

                localStorage.setItem(
                    "token",
                    response.data.access_token
                )

                localStorage.setItem(
                    "user",
                    JSON.stringify(response.data.user)
                )

                this.$router.push("/complete-profile")

            }

            catch (error) {

                this.error = error.response.data.message

            }

        }

    }

}

</script>
