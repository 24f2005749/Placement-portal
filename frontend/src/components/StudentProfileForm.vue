<template>
	<div class="card p-4">
		<h3>
			Complete Student Profile
		</h3>
		<form @submit.prevent="submit">
			<input v-model="full_name" class="form-control mb-3" placeholder="Full Name">
			<input v-model="roll_number" class="form-control mb-3" placeholder="Roll Number">
			<div class="mb-3">
				<label class="form-label">
					Branch
				</label>
				<select v-model="branch" class="form-select" required>
					<option value="" disabled>
						Select Branch
					</option>
					<option v-for="branch in branches" :key="branch.id" :value="branch.id">
						{{ branch.name }}
					</option>
				</select>
			</div>
			<input v-model="cgpa" type="number" step="0.01" class="form-control mb-3" placeholder="CGPA">
			<input v-model="graduation_year" type="number" class="form-control mb-3" placeholder="Graduation Year">
			<input v-model="phone" class="form-control mb-3" placeholder="Phone">
			<input v-model="resume" type="url" class="form-control mb-3" placeholder="Resume URL">
			<button class="btn btn-primary" :disabled="submitting">
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
			full_name: "",
			roll_number: "",
			branch: "",
			branches: [],
			cgpa: "",
			graduation_year: "",
			phone: "",
			resume: "",
			editing: false,
			submitting: false,
			error: ""
		}
	},
	async mounted() {
		try {
			const branches = await api.get("/branches")
			this.branches = branches.data
		}
		catch (error) {
			this.error = "Failed to load branches"
			console.error(error)
		}
		try {
			const response = await api.get("/student/profile")
			this.full_name = response.data.full_name
			this.roll_number = response.data.roll_number
			this.branch = response.data.branch_id
			this.cgpa = response.data.cgpa
			this.graduation_year = response.data.graduation_year
			this.phone = response.data.phone
			this.resume = response.data.resume
			this.editing = true
		}
		catch (error) {
			if (error.response && error.response.status == 404) {
				this.editing = false
			} else {
				this.error = "Failed to load profile"
			}
		}
	},
	methods: {
		async submit() {
			this.submitting = true
			this.error = ""
			const body = {
				full_name: this.full_name,
				roll_number: this.roll_number,
				branch: this.branch,
				cgpa: this.cgpa,
				graduation_year: this.graduation_year,
				phone: this.phone,
				resume: this.resume
			}
			if (!body.full_name || !body.roll_number || !body.branch || !body.cgpa || !body.graduation_year) {
				this.error = "Please fill all required fields"
				this.submitting = false
				return
			}
			try {
				if (this.editing) {
					await api.put("/student/profile", body)
					showToast("Profile updated successfully", "success")
				}
				else {
					await api.post("/student/profile", body)
					const user = JSON.parse(localStorage.getItem("user"))
					user.profile_completed = true
					localStorage.setItem(
						"user",
						JSON.stringify(user)
					)
					showToast("Profile created successfully", "success")
				}
				this.$router.push("/student/dashboard")
			}
			catch (error) {
				this.error = error.response?.data?.message || "Something went wrong"
				console.log(error.response)
			}
			finally {
				this.submitting = false
			}
		}
	}
}
</script>
