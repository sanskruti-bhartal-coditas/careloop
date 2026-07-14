package org.project.javabackend.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.project.javabackend.dto.request.AccountRequestDto;
import org.project.javabackend.dto.request.AppointmentTypeRequestDto;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.service.AdminService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/admin")
public class AdminController {

    private final AdminService adminService;

    // create account
    @PostMapping("/account")
    public ResponseEntity<GenericResponse> createAccount(@Valid @RequestBody AccountRequestDto accountRequestDto){
        return ResponseEntity.ok(adminService.createAccount(accountRequestDto));
    }


    // delete account

    @DeleteMapping("/account/{id}")
    public ResponseEntity<GenericResponse> deleteAccount(@PathVariable Long id){
        return ResponseEntity.status(HttpStatus.NO_CONTENT).body(adminService.deleteAccount(id));
    }


    // create type of appointments
    @PostMapping("/add-appointment-type")
    public ResponseEntity<GenericResponse> addAppointmentType(@Valid @RequestBody AppointmentTypeRequestDto appointmentTypeRequestDto){
        return ResponseEntity.ok(adminService.createAppointmentType(appointmentTypeRequestDto));
    }

}
