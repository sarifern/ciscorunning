from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image

from .models import (
	FSPartnerWorkoutForm,
	PartnerWorkoutConfirmationForm,
	PartnerWorkoutForm,
)


def make_test_image(name="evidence.png"):
	image_data = BytesIO()
	Image.new("RGB", (2, 2), color="white").save(image_data, format="PNG")
	return SimpleUploadedFile(name, image_data.getvalue(), content_type="image/png")


class PartnerWorkoutEvidenceFormTests(SimpleTestCase):
	def test_submitter_evidence_is_required_and_selfie_is_optional(self):
		for form_class in (PartnerWorkoutForm, FSPartnerWorkoutForm):
			with self.subTest(form=form_class.__name__):
				form = form_class()
				self.assertTrue(form.fields["photo_evidence"].required)
				self.assertFalse(form.fields["partner_selfie"].required)

	def test_partner_evidence_is_always_required(self):
		form = PartnerWorkoutConfirmationForm(data={}, files={})

		self.assertFalse(form.is_valid())
		self.assertIn("partner_photo_evidence", form.errors)

	def test_partner_must_supply_selfie_only_when_submitter_did_not(self):
		required_form = PartnerWorkoutConfirmationForm(
			data={},
			files={"partner_photo_evidence": make_test_image()},
			require_selfie=True,
		)
		optional_form = PartnerWorkoutConfirmationForm(
			data={},
			files={"partner_photo_evidence": make_test_image()},
			require_selfie=False,
		)

		self.assertFalse(required_form.is_valid())
		self.assertIn("partner_selfie", required_form.errors)
		self.assertTrue(optional_form.is_valid(), optional_form.errors)
