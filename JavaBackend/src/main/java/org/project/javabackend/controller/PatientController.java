package org.project.javabackend.controller;

import lombok.RequiredArgsConstructor;
import org.project.javabackend.dto.request.AppointmentRequestDto;
import org.project.javabackend.dto.request.PatientProfileRequestDto;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.service.AppointmentService;
import org.project.javabackend.service.PatientService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/patient")
public class PatientController {

    private final PatientService patientService;
    private final AppointmentService appointmentService;

    // profile update
    @PostMapping("/profile")
    public ResponseEntity<GenericResponse> addProfile(PatientProfileRequestDto profileRequestDto){
        return ResponseEntity.ok(patientService.addProfile(profileRequestDto));
    }

    // new appointment request
    @PostMapping("/appointment")
    public ResponseEntity<GenericResponse> requestAppointment(AppointmentRequestDto appointmentRequestDto){
        return ResponseEntity.ok(appointmentService.createAppointment(appointmentRequestDto));
    }

   //  see the appointments
    @GetMapping("/appointments")



    // appointment based on id
    @GetMapping("/appointments/{id}")

//    public ResponseEntity<>

    // reschedule post

}
