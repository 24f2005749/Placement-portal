<template>

    <DashboardLayout>

        <Loader v-if="loading" />

        <div v-else>

            <PageTitle :title="drive.title" />

            <div class="card">

                <div class="card-body">

                    <h5>

                        {{ drive.company_name }}

                    </h5>

                    <p>

                        {{ drive.job_description }}

                    </p>

                    <p>

                        <strong>Package:</strong>

                        ₹ {{ drive.salary_package }} LPA

                    </p>

                    <p>

                        <strong>Location:</strong>

                        {{ drive.location }}

                    </p>

                    <p>

                        <strong>CGPA Required:</strong>

                        {{ drive.eligibility_cgpa }}

                    </p>

                    <p>

                        <strong>Graduation Year:</strong>

                        {{ drive.eligibility_year }}

                    </p>

                    <p class="text-danger">

                        <strong>Deadline:</strong>

                        {{ formatDate(drive.application_deadline) }}

                    </p>

                    <p v-if="deadlinePassed" class="text-danger">

                        Application deadline has passed.

                    </p>

                    <p v-if="drive.eligible === false && drive.eligibility_message" class="text-warning">

                        {{ drive.eligibility_message }}

                    </p>

                    <button class="btn btn-success" @click="apply"
                        :disabled="applying || drive.eligible === false || deadlinePassed">

                        {{ applying ? "Applying..." : "Apply" }}

                    </button>

                </div>

            </div>

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>

        </div>

    </DashboardLayout>

</template>

<script>
import api from "@/services/api"
import DashboardLayout from "@/layouts/DashboardLayout.vue"
import PageTitle from "@/components/PageTitle.vue"
import Loader from "@/components/Loader.vue"

export default {
    components: {
        DashboardLayout,
        PageTitle,
        Loader
    },

    data() {
        return {
            drive: {},
            loading: true,
            applying: false,
            error: ""
        }
    },

    computed: {
        deadlinePassed() {
            if (this.drive.deadline_passed === true) return true

            const deadline = this.deadlineDate()
            const today = new Date()
            today.setHours(0, 0, 0, 0)

            return deadline ? deadline < today : false
        }
    },

    async mounted() {
        await this.loadDrive()
    },

    methods: {
        async loadDrive() {
            try {
                const response = await api.get("/student/drives/" + this.$route.params.id)
                this.drive = response.data
            } catch (error) {
                this.error = error.response?.data?.message || "Failed to load drive"
            } finally {
                this.loading = false
            }
        },

        async apply() {
            this.applying = true
            this.error = ""

            try {
                await api.post("/student/applications", {
                    drive_id: this.drive.id
                })

                alert("Applied Successfully!")
                this.$router.push("/student/applications")
            } catch (error) {
                this.error = error.response?.data?.message || "Failed to apply"
                console.error(error)
            } finally {
                this.applying = false
            }
        },

        deadlineDate() {
            if (!this.drive.application_deadline) return null

            const match = String(this.drive.application_deadline).match(/^(\d{4})-(\d{2})-(\d{2})/)
            if (!match) return null

            return new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]))
        },

        formatDate(value) {
            if (!value) return ""

            const date = this.deadlineDate() || new Date(value)
            if (Number.isNaN(date.getTime())) return value

            return date.toLocaleDateString()
        }
    }
}
</script>
