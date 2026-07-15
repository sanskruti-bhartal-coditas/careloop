package org.project.javabackend.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.project.javabackend.dto.request.AppointmentRequestDto;
import org.project.javabackend.dto.request.PatientProfileRequestDto;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.service.AppointmentService;
import org.project.javabackend.service.PatientService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/patient")
public class PatientController {

    private final PatientService patientService;
    private final AppointmentService appointmentService;

    // profile update
    @PostMapping("/profile")
    public ResponseEntity<GenericResponse> addProfile(@Valid @RequestBody PatientProfileRequestDto profileRequestDto){
        return ResponseEntity.ok(patientService.addProfile(profileRequestDto));
    }

    // new appointment request
    @PostMapping("/appointment")
    public ResponseEntity<GenericResponse> requestAppointment(@Valid @RequestBody AppointmentRequestDto appointmentRequestDto){
        return ResponseEntity.ok(appointmentService.createAppointment(appointmentRequestDto));
    }

   //  see the appointments
//    @GetMapping("/appointments")
//    public ResponseEntity<>
//
//
//    // appointment based on id
//    @GetMapping("/appointments/{id}")

//    public ResponseEntity<>

    // reschedule post

}
