<template>
    <div class="card p-4">
        <h3>
            {{ editing ? "Edit Company Profile" : "Complete Company Profile" }}
        </h3>
        <form @submit.prevent="submit">
            <input v-model="company_name" class="form-control mb-3" placeholder="Company Name">
            <input v-model="website" class="form-control mb-3" placeholder="Website">
            <input v-model="hr_name" class="form-control mb-3" placeholder="HR Name">
            <input v-model="hr_email" class="form-control mb-3" placeholder="HR Email">
            <textarea v-model="description" class="form-control mb-3" placeholder="Description"></textarea>
            <button class="btn btn-success" :disabled="submitting">

                {{ submitting ? "Saving..." : "Save" }}

            </button>

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
        </form>
    </div>
</template>
<script>

import api from "@/services/api"
import { showToast } from "@/utils/toast"

export default {
    data() {
        return {
            company_name: "",
            website: "",
            hr_name: "",
            hr_email: "",
            description: "",
            editing: false,
            submitting: false,
            error: ""
        }
    },
    async mounted() {
        await this.loadProfile()
    },
    methods: {
        async loadProfile() {
            try {
                const response = await api.get("/company/profile")

                this.company_name = response.data.company_name
                this.website = response.data.website
                this.hr_name = response.data.hr_name
                this.hr_email = response.data.hr_email
                this.description = response.data.description

                this.editing = true

            }

            catch (error) {

                if (error.response && error.response.status == 404) {

                    this.editing = false

                }

            }

        },

        async submit() {

            this.submitting = true
            this.error = ""

            const body = {

                company_name: this.company_name,
                website: this.website,
                hr_name: this.hr_name,
                hr_email: this.hr_email,
                description: this.description

            }

            try {

                if (this.editing) {

                    await api.put("/company/profile", body)
                    this.lastUpdated = new Date().toLocaleDateString()
                    showToast("Profile updated successfully", "success")

                }

                else {

                    await api.post("/company/profile", body)
                    const user = JSON.parse(localStorage.getItem("user"))
                    user.profile_completed = true
                    localStorage.setItem("user", JSON.stringify(user))

                    showToast("Profile created successfully", "success")

                }

                this.$router.push("/company/dashboard")

            }

            catch (error) {

                this.error = error.response?.data?.message || "Failed to save profile"

            }

            finally {

                this.submitting = false

            }
        }
    }
}

</script>
