<template>
    <div class="card border-0 shadow-sm">
        <div class="card-body">
            <Loader v-if="loading" />

            <div v-else-if="locked" class="alert alert-warning mb-0">
                This drive has already been approved and cannot be edited.
            </div>

            <form v-else @submit.prevent="submit" class="row g-3">
                <div v-if="error" class="col-12">
                    <div class="alert alert-danger">{{ error }}</div>
                </div>

                <div class="col-md-6">
                    <label class="form-label">Title</label>
                    <input v-model="form.title" class="form-control" required />
                </div>

                <div class="col-md-6">
                    <label class="form-label">Location</label>
                    <input v-model="form.location" class="form-control" />
                </div>

                <div class="col-12">
                    <label class="form-label">Job Description</label>
                    <textarea v-model="form.job_description" class="form-control" rows="5" required></textarea>
                </div>

                <div class="col-md-4">
                    <label class="form-label">Salary Package</label>
                    <div class="input-group">
                        <input
                            v-model.number="form.salary_package"
                            type="number"
                            step="0.01"
                            min="0"
                            max="100"
                            class="form-control"
                            placeholder="Example: 4.5"
                        />
                        <span class="input-group-text">LPA</span>
                    </div>
                </div>

                <div class="col-md-4">
                    <label class="form-label">Eligibility Year</label>
                    <input v-model.number="form.eligibility_year" type="number" class="form-control" />
                </div>

                <div class="col-md-4">
                    <label class="form-label">Eligibility CGPA</label>
                    <input v-model.number="form.eligibility_cgpa" type="number" step="0.01" min="0" max="10" class="form-control" />
                </div>

                <div class="col-md-6">
                    <label class="form-label">Application Deadline</label>
                    <input v-model="form.application_deadline" type="date" class="form-control" required />
                </div>

                <div class="col-md-6">
                    <label class="form-label">Drive Date</label>
                    <input v-model="form.drive_date" type="date" class="form-control" />
                </div>

                <div class="col-12">
                    <label class="form-label">Eligible Branches</label>
                    <div class="border rounded p-3">
                        <div v-if="branches.length === 0" class="text-muted">
                            No branches available.
                        </div>
                        <div v-else class="row g-2">
                            <div v-for="branch in branches" :key="branch.id" class="col-md-6 col-lg-4">
                                <div class="form-check">
                                    <input
                                        :id="'branch-' + branch.id"
                                        v-model="form.eligible_branches"
                                        class="form-check-input"
                                        type="checkbox"
                                        :value="branch.id"
                                    />
                                    <label class="form-check-label" :for="'branch-' + branch.id">
                                        {{ branch.name }}
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-12 d-flex gap-2">
                    <button class="btn btn-primary" :disabled="submitting">
                        {{ submitting ? "Saving..." : buttonText }}
                    </button>
                    <router-link class="btn btn-outline-secondary" to="/company/drives">
                        Cancel
                    </router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import api from "@/services/api"
import { showToast } from "@/utils/toast"
import Loader from "@/components/Loader.vue"

export default {
    components: {
        Loader
    },

    props: {
        mode: {
            type: String,
            required: true
        },
        driveId: {
            type: [String, Number],
            default: null
        }
    },

    data() {
        return {
            branches: [],
            form: {
                title: "",
                job_description: "",
                salary_package: null,
                location: "",
                eligibility_year: null,
                eligibility_cgpa: null,
                application_deadline: "",
                drive_date: "",
                eligible_branches: []
            },
            loading: true,
            submitting: false,
            error: "",
            locked: false
        }
    },

    computed: {
        buttonText() {
            return this.mode === "edit" ? "Update Drive" : "Create Drive"
        }
    },

    async mounted() {
        await this.loadInitialData()
    },

    methods: {
        async loadInitialData() {
            this.loading = true
            this.error = ""

            try {
                const branchesResponse = await api.get("/branches")
                this.branches = branchesResponse.data

                if(this.mode === "edit"){
                    const driveResponse = await api.get(`/company/drives/${this.driveId}`)
                    const drive = driveResponse.data

                    if(drive.approval_status === "approved"){
                        this.locked = true
                        return
                    }

                    this.form = {
                        title: drive.title || "",
                        job_description: drive.job_description || "",
                        salary_package: drive.salary_package,
                        location: drive.location || "",
                        eligibility_year: drive.eligibility_year,
                        eligibility_cgpa: drive.eligibility_cgpa,
                        application_deadline: this.toDateInput(drive.application_deadline),
                        drive_date: this.toDateInput(drive.drive_date),
                        eligible_branches: drive.eligible_branches || []
                    }
                }
            } catch (error) {
                this.error = error.response?.data?.message || "Failed to load drive form"
            } finally {
                this.loading = false
            }
        },

        toDateInput(value) {
            if(!value) return ""
            const stringValue = String(value)

            if(/^\d{4}-\d{2}-\d{2}/.test(stringValue)){
                return stringValue.slice(0, 10)
            }

            const parsed = new Date(stringValue)

            if(Number.isNaN(parsed.getTime())){
                return ""
            }

            return parsed.toISOString().slice(0, 10)
        },

        payload() {
            const body = { ...this.form }

            Object.keys(body).forEach(key => {
                if(body[key] === "") body[key] = null
            })

            return body
        },

        async submit() {
            if(this.form.salary_package && this.form.salary_package > 100){
                this.error = "Enter salary package in LPA, for example 4.5 instead of 45000."
                showToast(this.error, "danger")
                return
            }

            this.submitting = true
            this.error = ""

            try {
                let response

                if(this.mode === "edit"){
                    response = await api.put(`/company/drives/${this.driveId}`, this.payload())
                    showToast("Drive updated successfully", "success")
                    this.$router.push(`/company/drives/${this.driveId}`)
                } else {
                    response = await api.post("/company/drives", this.payload())
                    showToast("Drive created successfully", "success")
                    this.$router.push(`/company/drives/${response.data.drive_id}`)
                }
            } catch (error) {
                this.error = error.response?.data?.message || "Failed to save drive"
                showToast(this.error, "danger")
            } finally {
                this.submitting = false
            }
        }
    }
}
</script>
