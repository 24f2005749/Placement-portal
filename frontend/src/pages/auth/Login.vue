<template>
    <div class="container vh-100 d-flex justify-content-center align-items-center">

        <div class="card shadow p-4" style="width:400px;">

            <h3 class="text-center mb-4">
                Placement Portal
            </h3>

            <form @submit.prevent="login">

                <div class="mb-3">
                    <label class="form-label">
                        Email
                    </label>

                    <input
                        v-model="email"
                        type="email"
                        class="form-control"
                        required
                    >
                </div>

                <div class="mb-3">
                    <label class="form-label">
                        Password
                    </label>

                    <input
                        v-model="password"
                        type="password"
                        class="form-control"
                        required
                    >
                </div>

                <button
                    class="btn btn-primary w-100"
                    type="submit"
                >
                    Login
                </button>

            </form>

            <div
                v-if="error"
                class="alert alert-danger mt-3"
            >
                {{ error }}
            </div>

            <p class="text-center mt-3">

                Don't have an account?

                <router-link to="/register">
                    Register
                </router-link>

            </p>

        </div>

    </div>
</template>

<script>
import api from "@/services/api"

export default{

    data(){
        return{

            email:"",
            password:"",
            error:""

        }
    },

    methods:{

        async login(){

            this.error=""

            try{

                const response=await api.post("/login",{

                    email:this.email,
                    password:this.password

                })

                localStorage.setItem(
                    "token",
                    response.data.access_token
                )

                localStorage.setItem(
                    "user",
                    JSON.stringify(response.data.user)
                )

                const role=response.data.user.role

                if(role!="admin" && !response.data.user.profile_completed){

                    this.$router.push("/complete-profile")
                    return

                }

                if(role=="student"){

                    this.$router.push("/student/dashboard")

                }

                else if(role=="company"){

                    this.$router.push("/company/dashboard")

                }

                else{

                    this.$router.push("/admin/dashboard")

                }

            }

            catch(error){

                if(error.response){

                    this.error=error.response.data.message

                }

                else{

                    this.error="Server not responding"

                }

            }

        }

    }

}
</script>
